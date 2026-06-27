#!/usr/bin/env python3
"""Local deterministic stages for the spritesheet workflow."""

from __future__ import annotations

import argparse
from filecmp import cmp
from pathlib import Path
from shutil import copy2, rmtree
from statistics import median

from PIL import Image, ImageDraw, ImageSequence


ALPHA_THRESHOLD = 8
SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
}


def alpha_bbox(image: Image.Image, threshold: int = ALPHA_THRESHOLD):
    alpha = image.convert("RGBA").getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    return mask.getbbox()


def require_bbox(image: Image.Image, label: Path | str):
    box = alpha_bbox(image)
    if box is None:
        raise ValueError(f"No visible foreground found in {label}")
    return box


def slice_sheet(
    sheet_path: Path,
    output_dir: Path,
    animation_name: str,
    columns: int,
    rows: int,
    allow_overwrite: bool,
) -> None:
    if not sheet_path.is_file():
        raise FileNotFoundError(f"Spritesheet not found: {sheet_path}")

    with Image.open(sheet_path) as sheet:
        sheet.load()
        width, height = sheet.size
        if width % columns != 0:
            raise ValueError(f"Sheet width {width}px is not divisible by {columns}.")
        if height % rows != 0:
            raise ValueError(f"Sheet height {height}px is not divisible by {rows}.")

        frame_width = width // columns
        frame_height = height // rows
        frame_count = columns * rows

        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths = [
            output_dir / f"{animation_name}-{index:03d}.png"
            for index in range(frame_count)
        ]
        refuse_overwrite(output_paths, allow_overwrite)

        for index, output_path in enumerate(output_paths):
            row = index // columns
            column = index % columns
            box = (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
            sheet.crop(box).save(output_path)

    print(f"Sliced {frame_count} frames into {output_dir}")


def remove_background(
    input_dir: Path,
    output_dir: Path,
    animation_name: str,
    key_color: tuple[int, int, int],
    tolerance: int,
    allow_overwrite: bool,
) -> None:
    sources = ordered_frames(input_dir, animation_name)
    if not sources:
        raise FileNotFoundError(f"No frames found in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = [output_dir / source.name for source in sources]
    refuse_overwrite(output_paths, allow_overwrite)

    for source, output_path in zip(sources, output_paths):
        rgba = Image.open(source).convert("RGBA")
        pixels = rgba.load()
        for y in range(rgba.height):
            for x in range(rgba.width):
                red, green, blue, alpha = pixels[x, y]
                matches_key = (
                    abs(red - key_color[0]) <= tolerance
                    and abs(green - key_color[1]) <= tolerance
                    and abs(blue - key_color[2]) <= tolerance
                )
                if matches_key:
                    pixels[x, y] = (red, green, blue, 0)
        rgba.save(output_path)

    print(f"Removed background from {len(sources)} frames into {output_dir}")


def normalize(
    input_dir: Path,
    output_dir: Path,
    animation_name: str,
    columns: int,
    rows: int,
    canvas_width: int,
    canvas_height: int,
    target_anchor_x: float,
    target_bottom_y: int,
    preserve_vertical: bool,
    fps: int,
    allow_overwrite: bool,
) -> None:
    sources = ordered_frames(input_dir, animation_name)
    expected_count = columns * rows
    if len(sources) != expected_count:
        raise ValueError(f"Expected {expected_count} frames, found {len(sources)}.")

    frames: list[Image.Image] = []
    heights: list[int] = []
    for source in sources:
        opened = Image.open(source)
        if "A" not in opened.getbands():
            raise ValueError(f"Frame has no alpha channel: {source}")
        frame = opened.convert("RGBA")
        box = require_bbox(frame, source)
        heights.append(box[3] - box[1])
        frames.append(frame)

    output_dir.mkdir(parents=True, exist_ok=True)
    parent = output_dir.parent
    output_paths = [
        output_dir / f"{animation_name}-{index:03d}.png"
        for index in range(len(frames))
    ]
    atlas_path = parent / f"{animation_name}-normalized-atlas.png"
    contact_path = parent / f"{animation_name}-contact-sheet.png"
    gif_path = parent / f"{animation_name}-preview.gif"
    refuse_overwrite(output_paths + [atlas_path, contact_path, gif_path], allow_overwrite)

    normalized_frames: list[Image.Image] = []
    for index, frame in enumerate(frames):
        box = require_bbox(frame, sources[index])
        foreground = frame.crop(box)
        visible_width, visible_height = foreground.size
        paste_x = round(target_anchor_x - (visible_width / 2))
        if preserve_vertical:
            paste_y = box[1]
        else:
            paste_y = round(target_bottom_y - visible_height)

        if (
            paste_x < 0
            or paste_y < 0
            or paste_x + visible_width > canvas_width
            or paste_y + visible_height > canvas_height
        ):
            raise ValueError(
                f"Frame does not fit normalized canvas: {sources[index]} "
                f"foreground={foreground.size} paste=({paste_x}, {paste_y})"
            )

        canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
        canvas.alpha_composite(foreground, (paste_x, paste_y))
        canvas.save(output_paths[index])
        normalized_frames.append(canvas)

    build_atlas(normalized_frames, columns, rows).save(atlas_path)
    build_contact_sheet(normalized_frames, columns, canvas_width, canvas_height).save(
        contact_path
    )
    save_gif(normalized_frames, gif_path, fps)

    mode = "x-only, preserved vertical motion" if preserve_vertical else "x+y baseline"
    print(f"Normalized {len(normalized_frames)} frames into {output_dir}")
    print(f"Mode: {mode}")
    print(f"Median source visible height: {median(heights)}px")
    print(f"Atlas: {atlas_path}")
    print(f"Contact sheet: {contact_path}")
    print(f"GIF: {gif_path}")


def finalize(
    animation_name: str,
    columns: int,
    rows: int,
    allow_overwrite: bool,
    clean: bool,
) -> None:
    work_dir = Path("work") / animation_name
    frames_dir = work_dir / "005-normalized" / "frames"
    approved_gif = work_dir / "005-normalized" / f"{animation_name}-preview.gif"
    output_dir = Path("output") / animation_name

    if not frames_dir.is_dir():
        raise NotADirectoryError(f"Approved frames not found: {frames_dir}")
    if not approved_gif.is_file():
        raise FileNotFoundError(f"Approved GIF not found: {approved_gif}")

    frame_paths = ordered_frames(frames_dir, animation_name)
    if len(frame_paths) != columns * rows:
        raise ValueError(f"{len(frame_paths)} frames do not fill a {columns}x{rows} grid.")

    frames = []
    frame_size = None
    for path in frame_paths:
        opened = Image.open(path)
        if "A" not in opened.getbands():
            raise ValueError(f"Approved frame has no alpha channel: {path}")
        frame = opened.convert("RGBA")
        if frame_size is None:
            frame_size = frame.size
        elif frame.size != frame_size:
            raise ValueError(f"Frame size mismatch: {path}")
        frames.append(frame)

    output_dir.mkdir(parents=True, exist_ok=True)
    sheet_path = output_dir / f"{animation_name}-spritesheet.png"
    gif_path = output_dir / f"{animation_name}.gif"
    refuse_overwrite([sheet_path, gif_path], allow_overwrite)

    build_atlas(frames, columns, rows).save(sheet_path)
    copy2(approved_gif, gif_path)
    if not cmp(approved_gif, gif_path, shallow=False):
        raise ValueError("Final GIF is not byte-for-byte identical to approved preview.")

    if clean:
        rmtree(work_dir)

    print(f"Approved frames: {len(frames)}")
    print(f"Frame size: {frame_size[0]}x{frame_size[1]}px")
    print(f"Spritesheet: {sheet_path}")
    print(f"GIF: {gif_path}")
    if clean:
        print(f"Removed workspace: {work_dir}")


def process_approved(args: argparse.Namespace) -> None:
    work_dir = Path("work") / args.animation_name
    slice_dir = work_dir / "003-sliced"
    transparent_dir = work_dir / "004-transparent"
    normalized_dir = work_dir / "005-normalized" / "frames"

    slice_sheet(
        args.sheet,
        slice_dir,
        args.animation_name,
        args.columns,
        args.rows,
        args.allow_overwrite,
    )
    remove_background(
        slice_dir,
        transparent_dir,
        args.animation_name,
        args.key_color,
        args.tolerance,
        args.allow_overwrite,
    )
    normalize(
        transparent_dir,
        normalized_dir,
        args.animation_name,
        args.columns,
        args.rows,
        args.canvas_width,
        args.canvas_height,
        args.target_anchor_x,
        args.target_bottom_y,
        args.preserve_vertical,
        args.fps,
        args.allow_overwrite,
    )


def ordered_frames(directory: Path, animation_name: str) -> list[Path]:
    return sorted(
        path
        for path in directory.glob(f"{animation_name}-*.png")
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )


def refuse_overwrite(paths: list[Path], allow_overwrite: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not allow_overwrite:
        raise FileExistsError(
            f"Refusing to overwrite {existing[0]}; rerun with --allow-overwrite."
        )


def build_atlas(frames: list[Image.Image], columns: int, rows: int) -> Image.Image:
    if len(frames) != columns * rows:
        raise ValueError(f"{len(frames)} frames do not fill a {columns}x{rows} grid.")
    cell_width, cell_height = frames[0].size
    atlas = Image.new("RGBA", (columns * cell_width, rows * cell_height), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, ((index % columns) * cell_width, (index // columns) * cell_height))
    return atlas


def build_contact_sheet(
    frames: list[Image.Image],
    columns: int,
    canvas_width: int,
    canvas_height: int,
) -> Image.Image:
    rows = (len(frames) + columns - 1) // columns
    label_height = 24
    sheet = Image.new(
        "RGBA",
        (columns * canvas_width, rows * (canvas_height + label_height)),
        (32, 32, 32, 255),
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        x = (index % columns) * canvas_width
        y = (index // columns) * (canvas_height + label_height)
        sheet.alpha_composite(frame, (x, y))
        draw.text((x + 6, y + canvas_height + 4), f"{index:03d}", fill="white")
    return sheet


def save_gif(frames: list[Image.Image], output_path: Path, fps: int) -> None:
    gif_frames = []
    for frame in frames:
        background = Image.new("RGBA", frame.size, (32, 32, 32, 255))
        background.alpha_composite(frame)
        gif_frames.append(background.convert("P", palette=Image.Palette.ADAPTIVE))
    gif_frames[0].save(
        output_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=round(1000 / fps),
        loop=0,
        disposal=2,
    )


def parse_color(value: str) -> tuple[int, int, int]:
    if not value.startswith("#") or len(value) != 7:
        raise argparse.ArgumentTypeError("Use #RRGGBB format.")
    try:
        return (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16))
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use #RRGGBB format.") from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_stage_args(stage: argparse.ArgumentParser) -> None:
        stage.add_argument("--animation-name", required=True)
        stage.add_argument("--columns", type=int, required=True)
        stage.add_argument("--rows", type=int, required=True)
        stage.add_argument("--allow-overwrite", action="store_true")

    process = subparsers.add_parser(
        "process-approved",
        help="Run slice, background removal, and normalization after sheet approval.",
    )
    add_common_stage_args(process)
    process.add_argument("--sheet", type=Path, required=True)
    process.add_argument("--key-color", type=parse_color, default=(0, 255, 0))
    process.add_argument("--tolerance", type=int, default=0)
    process.add_argument("--canvas-width", type=int, default=256)
    process.add_argument("--canvas-height", type=int, default=256)
    process.add_argument("--target-anchor-x", type=float, default=128)
    process.add_argument("--target-bottom-y", type=int, default=236)
    process.add_argument(
        "--preserve-vertical",
        action="store_true",
        help=(
            "Center frames on the X axis only and preserve each frame's original "
            "vertical position for baked jump/hop/presentation motion."
        ),
    )
    process.add_argument("--fps", type=int, default=12)
    process.set_defaults(func=process_approved)

    finalize_parser = subparsers.add_parser(
        "finalize",
        help="Create final output assets from approved normalized frames.",
    )
    add_common_stage_args(finalize_parser)
    finalize_parser.add_argument("--keep-work", action="store_true")
    finalize_parser.set_defaults(
        func=lambda args: finalize(
            args.animation_name,
            args.columns,
            args.rows,
            args.allow_overwrite,
            not args.keep_work,
        )
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

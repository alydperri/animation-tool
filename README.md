# Game Animation Spritesheet Workflow

Create game-ready 2D animation assets from a static character image with a
repeatable, reviewable folder workflow.

This repo is a folder-based specialist for a common game-dev problem: getting
from "I have a character image" to "I have an approved animated GIF and
transparent spritesheet I can put in my game" without hand-writing the same
cleanup scripts every time.

## What It Solves

AI image generation can produce useful animation sheets, but raw outputs often
need careful follow-through:

- prompts must preserve character identity and action direction
- generated sheets must be checked before slicing
- chroma backgrounds need clean alpha removal
- frames need a stable canvas, anchor, and baseline
- GIF previews need human approval before final export
- temporary files should not leak into the final repo

This workflow turns that into an interpretable pipeline with two human review
checkpoints and deterministic local processing for everything after generation.

## Quickstart

1. Put your character reference image in `anchors/`.

   ```text
   anchors/my-character.png
   ```

2. Ask an agent to create the animation.

   ```text
   Create a walk-east animation for the character in anchors/my-character.png.
   ```

3. Review the generated spritesheet.

   If it looks wrong, ask for changes. If it looks right, approve it.

4. The agent runs deterministic cleanup automatically:

   ```text
   003 slice -> 004 remove background -> 005 normalize
   ```

5. Review the normalized GIF preview.

   If it works in motion, approve it.

6. Final assets are written to:

   ```text
   output/<animation-name>/
   ├── <animation-name>.gif
   └── <animation-name>-spritesheet.png
   ```

7. The temporary workspace for that animation is removed after final validation.

## Folder Map

```text
.
├── brief.md                 # Competition/client brief
├── identity.md              # What this specialist is
├── rules.md                 # Non-negotiable workflow rules
├── examples.md              # Copyable usage examples
├── AGENTS.md                # Agent routing and execution rules
├── anchors/                 # User-provided source images
├── configs/                 # Batch workflow config examples
├── demo/                    # Small completed example for reviewers
├── output/                  # Final approved assets
├── reference/               # Workflow contracts and stage details
├── tools/                   # Deterministic local helper scripts
├── work/                    # Disposable per-animation workspace
└── disposable/              # Disposable batch workspace
```

The competition-facing structure is intentional: `brief.md`, `identity.md`,
`rules.md`, `examples.md`, `reference/`, and this `README.md` are the core
folder-system interface.

## Demo

Completed examples are included in:

```text
demo/
├── walk-east/   # standard game-normalized walk cycle
└── jump-2/      # presentation GIF with preserved vertical jump motion
```

Use it to inspect the kind of asset this workflow produces before running your
own animation.

## Standard Workflow

```text
001 generate spritesheet
        ↓
user reviews generated sheet
        ↓ approved
003 slice sheet into frames
        ↓ automatic
004 remove chroma background
        ↓ automatic
005 normalize frames and build GIF preview
        ↓
user reviews normalized GIF
        ↓ approved
006 finalize assets and clean workspace
```

Why there is no step `002` in the normal path: `002` is reserved for an
experimental image-to-video workflow and is currently not part of the reliable
spritesheet pipeline.

## Review Checkpoints

Generated spritesheet review:

- checks character identity, pose direction, frame count, grid layout, and
  animation readability
- happens before slicing so malformed sheets do not enter the deterministic
  stages

Normalized GIF review:

- checks the animation in motion after alpha removal and anchoring
- happens before final assets are promoted into `output/`

## Image Generation Tooling

This folder system was built for use with ChatGPT/OpenAI image generation for
stage `001`. The later stages are local Python/Pillow processing and do not
depend on a specific chat product.

If you use Claude, another coding agent, or a different automation setup, you
need to provide an equivalent image-generation tool that can create the initial
spritesheet from the stage-001 prompt. Once that approved spritesheet exists,
the local cleanup and finalization workflow is the same.

## Local Commands

Image generation still requires an agent or image model. Once a generated sheet
is approved, the local helper can run the deterministic stages:

```bash
python3 tools/sprite_pipeline.py process-approved \
  --animation-name walk-east \
  --sheet work/walk-east/001-generated/walk-east-spritesheet.png \
  --columns 4 \
  --rows 2
```

This creates:

```text
work/walk-east/003-sliced/
work/walk-east/004-transparent/
work/walk-east/005-normalized/
```

For presentation GIFs or baked vertical motion, such as a jump where the GIF
itself should show the character rising and falling, preserve the frame's
vertical position and normalize only horizontal drift:

```bash
python3 tools/sprite_pipeline.py process-approved \
  --animation-name jump \
  --sheet work/jump/001-generated/jump-spritesheet.png \
  --columns 6 \
  --rows 4 \
  --fps 24 \
  --preserve-vertical
```

After the normalized GIF is approved:

```bash
python3 tools/sprite_pipeline.py finalize \
  --animation-name walk-east \
  --columns 4 \
  --rows 2
```

This creates final assets in `output/walk-east/` and removes `work/walk-east/`.

Useful options:

- `--allow-overwrite` permits regenerating a current stage.
- `--canvas-width` and `--canvas-height` set normalized runtime frame size.
- `--target-anchor-x` sets the horizontal anchor.
- `--target-bottom-y` sets the visible baseline.
- `--preserve-vertical` keeps baked up/down motion while still centering X.
- `--fps` sets GIF preview playback speed.
- `--keep-work` on `finalize` preserves the workspace for debugging.

## Batch Workflow

Use batch mode when you want to generate multiple candidates, rank them, and
finalize only the best outputs.

Start with:

```text
configs/batch-spritesheet.example.json
```

Batch stage contracts live in:

```text
reference/stages/batch/
```

Batch scratch work is disposable:

```text
disposable/batch/<animation-name>/
```

Final ranked outputs are written to:

```text
output/batch/<animation-name>/<rank-number>/
├── <animation-name>.gif
└── <animation-name>-spritesheet.png
```

## Requirements

- Python 3
- Pillow, installed with `python3 -m pip install Pillow`

Check your environment:

```bash
python3 --version
python3 -c "import PIL; print(PIL.__version__)"
```

If Pillow is missing:

```bash
python3 -m pip install Pillow
```

## What To Commit

Commit:

- `brief.md`, `identity.md`, `rules.md`, `examples.md`, `README.md`
- `reference/`
- `tools/`
- reusable configs
- intentional demo assets in `demo/`
- placeholder docs in `anchors/` and `output/`

Usually do not commit:

- `work/`
- `disposable/`
- generated outputs
- private anchor images
- temporary reference folders

## Where To Read Next

- `brief.md` explains the real problem this solves.
- `identity.md` explains what the specialist is.
- `rules.md` defines the workflow rules.
- `examples.md` gives copyable usage patterns.
- `reference/workflow.md` gives the pipeline contract.
- `reference/checklists.md` gives pre-submit and per-animation checks.
- `reference/stages/` contains the detailed stage procedures.

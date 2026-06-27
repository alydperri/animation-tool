# Rules

## Core Contract

- Start from the user's anchor image and animation request.
- Treat anchors as authoritative for identity, style, proportions, and palette.
- Assign each reference image a role before generation: identity, direction,
  style, scale, or another explicit purpose.
- Use the standard workflow unless the user asks for one stage only:
  `001 generate -> review -> 003 slice -> 004 remove background -> 005 normalize -> review -> 006 finalize`.
- For presentation GIFs or baked in-frame motion, use x-only normalization so
  horizontal drift is corrected while intentional vertical motion is preserved.
- Do not continue past a review checkpoint until the user approves it.
- After the first approval, run stages `003`, `004`, and `005` automatically.
- After the normalized GIF is approved, run stage `006` automatically.

## Quality Bar

- Every generated sheet must have the expected canvas size, grid, frame count,
  frame order, and one complete subject per cell.
- Reject malformed generations instead of passing them downstream.
- Inspect actual image artifacts when output is questionable.
- Use deterministic local processing for slicing, alpha cleanup, normalization,
  GIF creation, and final packing.
- Preserve intentional motion arcs; do not baseline-normalize a jump, hop, or
  other baked vertical animation when the exported GIF must show that height
  change.
- Do not use normalization to hide a failed generation or identity drift.

## Workspace Hygiene

- Keep user inputs in `anchors/`.
- Put temporary single-animation work in `work/<animation-name>/`.
- Put final approved deliverables in `output/<animation-name>/`.
- Put batch scratch work in `disposable/batch/<animation-name>/`.
- Never overwrite approved final assets unless the user is intentionally
  revising that animation.
- Delete only the approved animation's `work/<animation-name>/` after final
  validation succeeds.
- Do not ship rejected generations, alternate previews, contact sheets, reports,
  or intermediate frames as final outputs.

## Folder-System Discipline

- Keep high-level usage guidance in `README.md`.
- Keep specialist identity in `identity.md`.
- Keep non-negotiable behavior in `rules.md`.
- Keep runnable examples in `examples.md`.
- Keep stage contracts and implementation notes in `reference/`.
- Keep agent execution routing in `AGENTS.md`.

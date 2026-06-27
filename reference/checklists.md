# Checklists

Use these checklists before publishing the repo or finalizing an animation.

## Competition Submission

- `brief.md` exists at the repo root and is 250 words or fewer.
- `identity.md`, `rules.md`, `examples.md`, `reference/`, and `README.md`
  exist at the repo root.
- `README.md` explains the problem, who the folder is for, and how to use it.
- `rules.md` is the canonical behavior contract.
- `AGENTS.md` only handles agent bootstrapping and routing.
- Temporary reference folders are removed or ignored.
- Private anchors and generated work are not accidentally committed.
- Any committed generated assets are intentional demos under `demo/`.
- A stranger can understand the workflow without reading chat history.

## New Animation Run

- Anchor images are stored in `anchors/`.
- Each anchor has an assigned role before generation.
- Generated spritesheet matches the expected canvas, grid, and frame count.
- User approved the generated spritesheet before slicing.
- Sliced frames preserve order and dimensions.
- Background removal produces real alpha transparency.
- Normalized frames share a stable canvas, anchor, and baseline.
- User approved the normalized GIF before finalization.
- Final GIF and spritesheet validate in `output/<animation-name>/`.
- `work/<animation-name>/` is removed after final validation.

## Public Repo Hygiene

- No `.DS_Store` files.
- No `work/` or `disposable/` artifacts.
- No private `.env` files.
- No temporary reference materials.
- No generated outputs unless they are intentional demo assets under `demo/`.
- Runtime dependencies are documented in `README.md`.

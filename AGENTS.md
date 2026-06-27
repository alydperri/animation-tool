# AGENTS.md

## Agent Bootstrap

Before running a workflow, read these files in order:

1. `identity.md`
2. `rules.md`
3. The applicable stage file under `reference/stages/`

## Stage Routing

- Spritesheet generation from anchor images:
  `reference/stages/001-generate-spritesheet.md`
- Image-to-video animation:
  `reference/stages/002-generate-animation-i2v.md`
- Spritesheet slicing:
  `reference/stages/003-slice-spritesheet.md`
- Chroma background removal:
  `reference/stages/004-remove-backgrounds-with-pillow.md`
- Frame normalization and preview:
  `reference/stages/005-normalize-animation-frames.md`
- Final spritesheet packaging and cleanup:
  `reference/stages/006-finalize-animation-assets.md`
- Batch spritesheet generation, ranking, and finalization:
  `reference/stages/batch/001-batch-create-spritesheets.md`,
  `reference/stages/batch/002-batch-stack-rank-spritesheets.md`, and
  `reference/stages/batch/003-batch-process-ranked-candidates.md`

## Routing Rules

For a complete spritesheet request, start at stage `001` and continue through
the full workflow described in `rules.md`. Do not treat each stage as an
unrelated standalone task unless the user explicitly requests only that
operation.

For a batch spritesheet request, follow the stage files under
`reference/stages/batch/` in numbered order.

## Local Tooling

Image-processing stages use Python 3 and Pillow. Check the environment with:

```bash
python3 --version
python3 -c "import PIL; print(PIL.__version__)"
```

Use `tools/sprite_pipeline.py` for deterministic local processing when a stage
can be handled by the helper.

Stage `001` assumes ChatGPT/OpenAI image generation is available. If the active
agent environment does not provide it, use an equivalent image-generation tool
or stop and explain the missing capability.

## Documentation Changes

When changing the workflow contract, update every affected document so the
handoffs, paths, checkpoints, and cleanup behavior remain consistent.

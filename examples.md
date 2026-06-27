# Examples

## Single Animation

1. Put the source character image in `anchors/`.
2. Ask the agent:

   ```text
   Create a walk-east animation for the character in anchors/cat-identity.png.
   ```

3. Review the generated spritesheet checkpoint.
4. If it looks right, say:

   ```text
   looks good
   ```

5. Review the normalized GIF checkpoint.
6. If it works in motion, say:

   ```text
   approved
   ```

7. Final assets appear in:

   ```text
   output/walk-east/
   ├── walk-east.gif
   └── walk-east-spritesheet.png
   ```

## Included Demo

The repo includes a completed example:

```text
demo/walk-east/
demo/jump-2/
```

Use these as expected shapes of finished runs: `walk-east` for standard
game-normalized output, and `jump-2` for preserved vertical motion in a
presentation GIF.

## Useful Requests

```text
Create an 8-frame idle animation for anchors/hero.png.
```

```text
Create a 12-frame dash-east animation. Keep the character centered in each
cell because the engine will move the sprite.
```

```text
Use anchors/character.png for identity and anchors/run-pose.png only for
directional body bias. Do not copy the pose exactly.
```

```text
The normalized GIF is too jumpy. Re-anchor the body center and rebuild the
preview before finalizing.
```

## Deterministic Local Commands

After a generated sheet is approved, the local helper can run the deterministic
cleanup stages:

```bash
python3 tools/sprite_pipeline.py process-approved \
  --animation-name walk-east \
  --sheet work/walk-east/001-generated/walk-east-spritesheet.png \
  --columns 4 \
  --rows 2
```

After the normalized GIF is approved:

```bash
python3 tools/sprite_pipeline.py finalize \
  --animation-name walk-east \
  --columns 4 \
  --rows 2
```

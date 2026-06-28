# Ghost Sample

This folder contains a small animation set for a ghost character used in a
game. These assets were created with the same workflow in another run of this
folder system.

Unlike the smaller demos, this sample shows a more realistic character pack:
some animations include final spritesheets, while others include only the GIF
preview because committing every spritesheet would be noisy.

All GIF previews in this folder use transparent backgrounds.

## Anchors

| File | Role |
| --- | --- |
| `forward-anchor.png` | Front-facing identity/style anchor |
| `directional-anchor.png` | East-facing direction/pose anchor |

## Animations

| Animation | Preview | Spritesheet | Notes |
| --- | --- | --- | --- |
| Idle east | `idle-east.gif` | `idle-east-spritesheet.png` | 16-frame subtle idle loop |
| Dash east | `dash-east.gif` | `dash-east-spritesheet.png` | 12-frame movement animation |
| Cast curse | `cast-curse-002.gif` | `cast-curse-002-spritesheet.png` | 12-frame character action |
| Curse VFX | `curse-vfx-001-batch-003.gif` | Not included | 24-frame supporting effect |

## Asset Details

```text
idle-east.gif                  314 x 314, 16 frames
idle-east-spritesheet.png      1256 x 1256
dash-east.gif                  314 x 314, 12 frames
dash-east-spritesheet.png      1256 x 942
cast-curse-002.gif             512 x 512, 12 frames
cast-curse-002-spritesheet.png 2048 x 1536
curse-vfx-001-batch-003.gif    312 x 312, 24 frames
```

This sample is useful for judging the workflow as a practical game-animation
tool rather than only a single-output demo.

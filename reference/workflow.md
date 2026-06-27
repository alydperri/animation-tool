# Workflow Contract

## Standard Spritesheet Pipeline

```text
001 generate spritesheet
    -> user reviews generated sheet
003 slice sheet into frames
004 remove chroma background
005 normalize frames and build preview
    -> user reviews normalized GIF
006 finalize assets and remove workspace
```

## Review Gates

There are two human approval points:

1. Generated spritesheet approval after stage `001`.
2. Normalized GIF approval after stage `005`.

All other stages are deterministic cleanup and validation steps. Run them
automatically after the relevant approval.

## Final Deliverables

```text
output/<animation-name>/
├── <animation-name>.gif
└── <animation-name>-spritesheet.png
```

The final GIF is copied from the approved stage-005 preview. The final
spritesheet is rebuilt from the approved normalized PNG frames.

## X-Only Normalization Path

Use this path when the exported GIF should preserve baked in-frame movement,
such as a jump where the character visibly rises and falls inside the frame.

The pipeline stays the same, but stage `005` uses x-only normalization:

```text
001 generate spritesheet
    -> user reviews generated sheet
003 slice sheet into frames
004 remove chroma background
005 center frames on X while preserving original Y positions
    -> user reviews requested-fps GIF
006 finalize assets and remove workspace
```

This corrects horizontal jitter while preserving the intentional vertical arc.
Do not use full baseline normalization for presentation GIFs where the height
change is part of the desired animation.

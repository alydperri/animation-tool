# Stage Contracts

These files are the detailed procedures behind the high-level workflow.

Use them when running the pipeline manually, debugging a failed stage, or
changing the workflow contract.

```text
001-generate-spritesheet.md
002-generate-animation-i2v.md
003-slice-spritesheet.md
004-remove-backgrounds-with-pillow.md
005-normalize-animation-frames.md
006-finalize-animation-assets.md
batch/
```

The reliable default path is:

```text
001 -> review -> 003 -> 004 -> 005 -> review -> 006
```

`002` is currently documented but not part of the recommended path.

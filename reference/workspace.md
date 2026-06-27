# Workspace Contract

## Inputs

`anchors/` holds user-provided source images. Preserve these files.

## Temporary Work

`work/<animation-name>/` holds disposable artifacts for one animation:

```text
work/<animation-name>/
├── 001-generated/
├── 003-sliced/
├── 004-transparent/
└── 005-normalized/
```

Delete this animation workspace only after final validation succeeds.

## Final Output

`output/<animation-name>/` holds approved deliverables only:

```text
output/<animation-name>/
├── <animation-name>.gif
└── <animation-name>-spritesheet.png
```

## Batch Work

Batch scratch files live in `disposable/batch/<animation-name>/`.
Final ranked batch outputs live in:

```text
output/batch/<animation-name>/<rank-number>/
```

## Repository Hygiene

Do not commit:

- `work/`
- `disposable/`
- generated output assets unless intentionally sharing examples
- local temp/reference folders
- `.DS_Store`

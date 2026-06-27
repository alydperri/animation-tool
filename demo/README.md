# Demo

This folder contains completed examples so reviewers can see what the
workflow produces without running image generation.

```text
demo/
├── walk-east/
│   ├── cat-identity.png
│   ├── walk-east.gif
│   └── walk-east-spritesheet.png
└── jump-2/
    ├── spider-identity.png
    ├── jump-2.gif
    └── jump-2-spritesheet.png
```

`walk-east` follows the standard game-normalized workflow:

```text
anchor image -> generated sheet -> approved GIF -> final spritesheet
```

`jump-2` shows the presentation-GIF path, where horizontal drift is corrected
but the baked vertical jump motion is preserved.

The runtime spritesheets are transparent PNG output. The GIFs are the human
review previews.

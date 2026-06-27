# Brief

Making game animation assets from a single character image is slow and fussy. I
can usually get a decent generated spritesheet, but the real cost is everything
after that: checking the grid, slicing frames, removing chroma backgrounds,
normalizing pivots and baselines, building a GIF for review, exporting a final
spritesheet, and cleaning up disposable files without losing the source image.

I need a folder-based specialist that turns an anchor image plus an animation
request into production-ready game assets with clear human review checkpoints.
The system should preserve character identity, make direction and timing
explicit, use deterministic local processing for all cleanup stages, and leave
behind only the approved GIF and spritesheet.

I have tried doing this manually with ad hoc prompts and one-off scripts. It
works once, but it is too easy to forget a validation step, keep messy
intermediates, or produce assets that are hard to reuse in a game project.

This repo solves that by packaging the workflow as an interpretable folder
system: identity, rules, examples, reference contracts, numbered stages, and
local tooling that a new teammate can follow without hand-holding.

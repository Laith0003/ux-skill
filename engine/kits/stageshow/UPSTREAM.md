# Where this kit comes from

This folder is the `kit/` folder of Stageshow by Benji Taylor
(https://github.com/benjitaylor/skills), at commit
802057409787133703c56001080169e347305572 (2026-10-31), under the MIT
License in `LICENSE` beside this file.

Two changes were made to it, and nothing else:

1. The brand registry (`brands/`) and the `BrandMark` part are left out.
   They carry other companies' marks under their owners' own terms, not
   under the MIT License. Use the product's own artwork in their place.
2. Its few non-ASCII glyphs are written as escapes in code (the keycap
   symbols, the minus sign, the multiplication sign, the bullet, the
   terminal prompt) and as plain words in comments. What renders is the
   same.

The kit needs `react`, `react-dom` and `lucide-react` (0.468.0 upstream)
in the project. Import it from `index.ts`; each part brings its own CSS.

`uxskill kit stageshow --out <folder> --from design-system/tokens.json`
writes this kit into a project with `stageshow-look.css`, the system's
look, beside it. Load that file after `stageshow.css` and give each stage
the class: `<Stage className="ux-look">`. When the system changes, add
`--look-only` to rewrite just the look, leaving every kit file as it is.

To update the kit, copy `kit/` from a newer commit, make the two changes
again, and put the new commit above. `tests/test_stageshow_kit.py` checks
that no brand mark came back, that every file is ASCII and that every
relative import still resolves.

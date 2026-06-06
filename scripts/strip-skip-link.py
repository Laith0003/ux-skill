"""Strip the broken `Skip to content` link from every HTML page.

User asked it removed because it renders awkwardly. Removes:
  - The <a class="skip-link"> element wherever it appears
  - The CSS rule `.skip-link { ... }` block (idempotent — only if found)

a11y note: a skip-link is an a11y net for keyboard users on long pages.
Removing it at the user's explicit request. If we want it back later,
this script's commit serves as a marker.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent


# Match: optional whitespace, the <a class="skip-link"...>...</a> element,
# and any trailing newline up to the next non-blank line.
SKIP_LINK_TAG = re.compile(
    r'^\s*<a\s+href="#main"\s+class="skip-link">[^<]+</a>\s*\n?',
    re.MULTILINE,
)

# Match a `.skip-link { ... }` block (greedy until the closing brace on its own line)
SKIP_LINK_CSS = re.compile(
    r'\s*\.skip-link\s*\{[^}]*\}\s*\n?\s*\.skip-link:focus\s*\{[^}]*\}\s*\n?'
    r'|\s*\.skip-link\s*\{[^}]*\}\s*\n?',
)


def strip(path: Path) -> tuple[bool, int]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    tag_swaps = len(SKIP_LINK_TAG.findall(text))
    text = SKIP_LINK_TAG.sub("", text)
    css_swaps = len(SKIP_LINK_CSS.findall(text))
    text = SKIP_LINK_CSS.sub("\n", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True, tag_swaps + css_swaps
    return False, 0


def main() -> None:
    targets = []
    for root_dir in (ROOT / "docs",):
        targets.extend(root_dir.rglob("*.html"))
    targets.sort()
    print(f"Stripping skip-link from {len(targets)} HTML files\n")
    changed = 0
    for p in targets:
        ok, swaps = strip(p)
        if ok:
            rel = str(p.relative_to(ROOT))
            print(f"ok   {rel:<60}  ({swaps} swaps)")
            changed += 1
    print(f"\nDone. {changed}/{len(targets)} files modified.")


if __name__ == "__main__":
    main()

"""Guard: nothing in the public engine repeats licensed foundation docs, names the
client engagement, or leaks a confidential term.

Four tests:
1. Shingle test against the private Ds/ corpus. Runs only on a machine that has
   the private source (CI skips). Per R24, a shingle only counts when it is
   mostly prose (see MIN_ALPHA_WORDS below) so public numeric vocabulary
   (cubic-bezier curves, rgba offsets, WCAG criterion titles) does not trip
   the guard.
2. A CI-safe unit test proving that R24 filter: a prose sentence still yields
   counted shingles, a numeric/token run does not. Needs no private source.
3. Name guard for the client company name and the vendor domain (plus its common
   misspelling). Runs everywhere, including CI, over every file `git ls-files`
   tracks. The forbidden names are assembled at runtime so this file never
   carries them as literals.
4. Private-term guard against `~/Code/ux-skill/ds-source/private-terms.txt`.
   Skips cleanly when that file is absent (CI, or any machine without the
   private source).
"""
import os
import re
import subprocess
from pathlib import Path

import pytest

PRIVATE = Path(os.path.expanduser("~/Code/ux-skill/ds-source/Ds"))
PRIVATE_TERMS = Path(os.path.expanduser("~/Code/ux-skill/ds-source/private-terms.txt"))
REPO = Path(__file__).resolve().parents[2]
THIS_FILE = Path(__file__).resolve()
SCAN = (
    "engine", "commands", "references", "agents", "docs", "README.md",
    "tests", "CHANGELOG.md", "skills", "data",
)
SCAN_SUFFIXES = (".py", ".md", ".html", ".json", ".css")

# Extensions that are never text, skipped without an open/decode attempt.
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".fig", ".zip",
    ".ttf", ".otf", ".woff", ".woff2", ".mp4", ".mov", ".webp",
}


# R24: a shingle only counts when most of it is prose. Cubic-bezier numbers,
# rgba shadow offsets, and WCAG criterion titles ("2.3.1 ...") are public
# vocabulary, not licensed phrasing, so require the majority of an 8-gram's
# words to be real alphabetic terms before treating it as a match.
MIN_ALPHA_WORDS = 5
_ALPHA_WORD = re.compile(r"[a-z']{3,}")


def shingles(text, n=8):
    w = re.findall(r"[a-z0-9']+", text.lower())
    result = set()
    for i in range(len(w) - n):
        gram = w[i:i + n]
        alpha = sum(1 for word in gram if _ALPHA_WORD.fullmatch(word))
        if alpha >= MIN_ALPHA_WORDS:
            result.add(" ".join(gram))
    return result


@pytest.mark.skipif(not PRIVATE.exists(), reason="private source not on this machine")
def test_no_eight_word_run_from_licensed_docs():
    licensed = set()
    for md in PRIVATE.glob("*/*.md"):
        licensed |= shingles(md.read_text(encoding="utf-8", errors="ignore"))
    hits = []
    for root in SCAN:
        base = REPO / root
        if not base.exists():
            continue
        if base.is_file():
            files = [base]
        else:
            files = [p for p in base.rglob("*") if p.suffix in SCAN_SUFFIXES]
        for f in files:
            if f.resolve() == THIS_FILE:
                continue
            shared = shingles(f.read_text(encoding="utf-8", errors="ignore")) & licensed
            if shared:
                hits.append(f"{f.relative_to(REPO)}: {sorted(shared)[0]}")
    assert not hits, "licensed phrasing found:\n" + "\n".join(hits[:20])


def test_shingle_filter_counts_prose_not_numbers():
    prose = (
        "the palette must always keep every semantic role pointing at a "
        "primitive step"
    )
    numeric = "cubic bezier 0 4 0 0 2 1 standard"
    assert shingles(prose), "prose sentence should still yield counted shingles"
    assert not shingles(numeric), "numeric/token run should yield no counted shingles"


def _tracked_files():
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout
    for rel in out.splitlines():
        if not rel:
            continue
        p = REPO / rel
        if p.suffix.lower() in BINARY_SUFFIXES:
            continue
        if not p.is_file():
            continue
        yield rel, p


def _read_text(p):
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


# Built at runtime, piece by piece, so the literal names never appear in this
# file's source (or anywhere else in the public repo).
_CLIENT_NAME = "".join(["m", "e", "r", "c", "a", "t", "o"])
_VENDOR_TLD = "".join(["s", "u", "r", "f"])
_VENDOR_DOMAIN = "".join(["d", "e", "s", "i", "g", "n", "s", "y", "s", "t", "e", "m", "s"]) + "." + _VENDOR_TLD
_VENDOR_DOMAIN_MISSPELLED = "".join(["d", "e", "s", "i", "g", "n", "s", "y", "s", "t", "e", "m"]) + "." + _VENDOR_TLD
FORBIDDEN_NAMES = (_CLIENT_NAME, _VENDOR_DOMAIN, _VENDOR_DOMAIN_MISSPELLED)


def test_no_confidential_names_anywhere():
    hits = []
    for rel, p in _tracked_files():
        if p.resolve() == THIS_FILE:
            continue
        text = _read_text(p)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            lower = line.lower()
            for name in FORBIDDEN_NAMES:
                if name in lower:
                    hits.append(f"{rel}:{lineno}")
                    break
    assert not hits, (
        "confidential name found -- remove the name; the method stays, "
        "the source is never named:\n" + "\n".join(hits[:50])
    )


@pytest.mark.skipif(not PRIVATE_TERMS.exists(), reason="private term list not on this machine")
def test_no_private_terms_anywhere():
    terms = []
    for line in PRIVATE_TERMS.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        terms.append(line.lower())
    hits = []
    for rel, p in _tracked_files():
        if p.resolve() == THIS_FILE:
            continue
        text = _read_text(p)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            lower = line.lower()
            for term in terms:
                if term in lower:
                    hits.append(f"{rel}:{lineno}: {term}")
                    break
    assert not hits, "private term found:\n" + "\n".join(hits[:50])

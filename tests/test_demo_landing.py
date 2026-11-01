"""The demo landing page shows fictional brands, never real businesses.

Each brand tile's initials belong to the name printed under it, and the page
never presents the brands as real businesses from a named country.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "demo" / "dot-landing.html", ROOT / "demo" / "dot-landing.blade.php"]
_TILE = re.compile(r'>([A-Z]{2})</span>\s*<span class="text-\[11px\] text-zinc-500">([^<]+)</span>')


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_each_tile_starts_with_its_brand_initial(page):
    tiles = _TILE.findall(page.read_text(encoding="utf-8"))
    assert len(tiles) == 3, f"{page.name}: expected the three brand tiles, found {tiles}"
    wrong = [(mark, name) for mark, name in tiles if mark[0] != name[0].upper()]
    assert not wrong, (f"{page.name}: tile initials do not match the brand under them: {wrong}; "
                       "write each tile as the initials of its brand's name")


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_the_brands_are_never_given_a_nationality(page):
    text = page.read_text(encoding="utf-8")
    assert "Jordanian" not in text, (f"{page.name} calls the fictional brands Jordanian; "
                                     "describe them without a nationality")

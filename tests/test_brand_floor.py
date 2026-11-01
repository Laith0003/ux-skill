"""The brand-fidelity floor counts the primary only where an element of the
page is painted with it: a rule whose selector matches an element, an inline
style or a color attribute. A stylesheet that only defines the primary, a
comment, an alternate or disabled stylesheet, one outside the page's folder,
or a selector that matches nothing does not count."""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.brand import score_brand_fidelity
from engine.brand.extract import BrandProfile

PRIMARY = "#1C64D9"
_BODY = ('<body><header><img src="img/logo.svg" width="120" height="32" '
         'alt="Fixture Client"></header><main><a class="cta" href="#go">Go</a>'
         '<img src="img/hero.jpg" width="800" height="600" alt="hero"></main></body></html>')


def _profile() -> BrandProfile:
    return BrandProfile(name="Fixture Client", primary=PRIMARY,
                        logo={"url": "img/logo.svg", "alt": "Fixture Client"})


def _score(tmp_path: Path, head: str, files: dict) -> dict:
    site = tmp_path / "site"
    site.mkdir(exist_ok=True)
    for rel, text in files.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    html = ("<!doctype html><html><head><style>.cta{background:#E11D48}</style>" + head
            + "</head>" + _BODY)
    return score_brand_fidelity(html, _profile(), base_dir=site)


_USED = {"site/used.css": ".cta{background:#1C64D9}"}


@pytest.mark.parametrize("head,files", [
    ('<link rel="stylesheet" href="unused.css">', {"site/unused.css": ":root{--brand-primary:#1C64D9}"}),
    ('<link rel="alternate stylesheet" href="used.css">', _USED),
    ('<!-- <link rel="stylesheet" href="used.css"> -->', _USED),
    ('<link rel="stylesheet" media="not all" href="used.css">', _USED),
    ('<link rel="stylesheet" href="note.css">', {"site/note.css": "/* brand #1C64D9 */ .cta{border:0}"}),
    ('<link rel="stylesheet" href="../other/used.css">', {"other/used.css": ".cta{background:#1C64D9}"}),
    ('<link rel="stylesheet" href="nomatch.css">', {"site/nomatch.css": ".nothing-here{background:#1C64D9}"}),
    ('<link rel="stylesheet" disabled href="used.css">', _USED),
    ('<link rel="stylesheet" href="focus.css">',
     {"site/focus.css": ":focus-visible{outline:2px solid #1C64D9}"}),
    ("", {}),
], ids=["defined-not-used", "alternate", "commented-link", "media-not-all", "css-comment",
        "outside-folder", "selector-matches-nothing", "disabled", "state-only-selector",
        "no-stylesheet"])
def test_the_floor_is_not_fooled(tmp_path: Path, head: str, files: dict) -> None:
    res = _score(tmp_path, head, files)
    assert res["passed"] is False and res["score"] == 65


@pytest.mark.parametrize("css", [
    ".cta{background:#1C64D9}",
    ":root{--brand-primary:#1C64D9;--a:var(--brand-primary)} .cta{background:var(--a)}",
    "@media (min-width: 1px){ main .cta:hover{color:rgb(28 100 217)} }",
    "@import 'deep.css';",
])
def test_a_used_primary_counts(tmp_path: Path, css: str) -> None:
    files = {"site/used.css": css, "site/deep.css": "a.cta{outline-color:#1c64d9}"}
    res = _score(tmp_path, '<link rel="stylesheet" href="used.css">', files)
    assert res["passed"] is True and res["score"] == 100


def test_the_detail_names_where_and_the_chain(tmp_path: Path) -> None:
    css = ":root{--brand-primary:#1C64D9;--a:var(--brand-primary)} .cta{background:var(--a)}"
    res = _score(tmp_path, '<link rel="stylesheet" href="used.css">', {"site/used.css": css})
    detail = next(f for f in res["findings"] if f["check"] == "primary_used")["detail"]
    assert ".cta { background }" in detail and "--a then --brand-primary" in detail


# ---------------------------------------------------------------- a page in a subfolder


def test_a_page_in_a_subfolder_reads_css_in_a_sibling_folder(tmp_path: Path) -> None:
    site = tmp_path / "site"
    (site / "en").mkdir(parents=True)
    (site / "css").mkdir()
    (site / "css" / "tokens.css").write_text(
        ":root{--brand-primary:#1C64D9} .cta{background:var(--brand-primary)}", encoding="utf-8")
    html = ('<!doctype html><html><head><link rel="stylesheet" href="../css/tokens.css">'
            "</head>" + _BODY)
    page_dir = site / "en"
    assert score_brand_fidelity(html, _profile(), base_dir=page_dir)["passed"] is False
    res = score_brand_fidelity(html, _profile(), base_dir=page_dir, root=site)
    assert res["passed"] is True and res["score"] == 100
    # the root still bounds what is read
    outside = score_brand_fidelity(html, _profile(), base_dir=page_dir, root=page_dir)
    assert outside["passed"] is False


def test_evaluate_takes_the_project_root(tmp_path: Path) -> None:
    from engine.evaluator import evaluate
    site = tmp_path / "site"
    (site / "en").mkdir(parents=True)
    (site / "css").mkdir()
    (site / "css" / "t.css").write_text(".cta{background:#1C64D9}", encoding="utf-8")
    html = ('<!doctype html><html><head><link rel="stylesheet" href="../css/t.css"></head>'
            + _BODY)
    ev = evaluate(html=html, brand_profile=_profile(), base_dir=str(site / "en"), root=str(site))
    assert ev.brand_passed is True


# ---------------------------------------------------------------- modern color syntax


@pytest.mark.parametrize("value", [
    "oklch(53.15% 0.1928 260.18)",
    "hsl(217 77% 48%)",
    "hsla(217, 77%, 48%, 1)",
    "color(srgb 0.1098 0.3922 0.851)",
    "oklab(0.5315 -0.0327 -0.19)",
], ids=["oklch", "hsl", "hsla", "color-srgb", "oklab"])
def test_a_primary_in_modern_syntax_counts_as_painted(tmp_path: Path, value: str) -> None:
    from engine.existing import normalize_hex
    primary = normalize_hex(value)
    css = ":root{--brand-primary:%s} .cta{background:var(--brand-primary)}" % value
    site = tmp_path / "site"
    site.mkdir()
    (site / "used.css").write_text(css, encoding="utf-8")
    html = ('<!doctype html><html><head><link rel="stylesheet" href="used.css"></head>'
            + _BODY)
    profile = BrandProfile(name="Fixture Client", primary=primary,
                           logo={"url": "img/logo.svg", "alt": "Fixture Client"})
    res = score_brand_fidelity(html, profile, base_dir=site)
    assert res["passed"] is True, (primary, res["findings"][0]["detail"])


# ---------------------------------------------------------------- residual decoys


@pytest.mark.parametrize("head,body_extra", [
    ('<style>.ghost{background:#1C64D9}</style>', '<div class="ghost" hidden></div>'),
    ('<style>.ghost{background:#1C64D9}</style>',
     '<template><div class="ghost"></div></template>'),
    ('<style>@media print{.cta{background:#1C64D9}}</style>', ""),
    ('<style>.cta::after{content:"#1C64D9"}</style>', ""),
], ids=["hidden", "template", "print-only", "content-string"])
def test_residual_decoys_do_not_count(head: str, body_extra: str) -> None:
    html = ("<!doctype html><html><head><style>.cta{background:#E11D48}</style>" + head
            + "</head>" + _BODY.replace("</main>", body_extra + "</main>"))
    res = score_brand_fidelity(html, _profile())
    assert res["passed"] is False and res["score"] == 65

"""Complaints: what the person said is wrong with a page, each kept as a
probe and closed only by measurement.

A budget calculator was rebuilt and its cookie card still floated over the
content, the one thing the brief asked to fix, and the work was called
done. Written as a complaint, the card keeps the check open (exit 3) until
the page measures clear; a probe the old page already passed proves nothing;
and the stop hook reads the last result without rendering."""
import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from engine.foundations.errors import InputError

pytest.importorskip("playwright")

from engine.complaints import KINDS, check_complaints, gate, load_complaints  # noqa: E402
from engine.render import RenderUnavailable  # noqa: E402

PAGE = ('<!doctype html><html lang="en"><head><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><style>{css}</style></head>'
        '<body style="margin:0"><main><h1 style="margin:80px 24px 16px">How much is left '
        'at the end of the month?</h1><form style="margin:0 24px"><label>Income '
        '<input name="income"></label><button>Work it out</button></form>'
        '<p style="margin:24px;height:900px">Everything stays in your browser.</p></main>'
        '{extra}</body></html>')
CARD = ('<div class="cookie" style="position:fixed;left:20%;right:20%;bottom:22%;padding:16px;'
        'background:#fff;border:1px solid #ccc">We use cookies. <button>Reject</button>'
        '<button>Accept</button></div>')
BAR = ('<div class="cookie" style="position:fixed;left:0;right:0;bottom:0;padding:12px 24px;'
       'background:#fff;border-top:1px solid #ccc">We use cookies. <button>Reject</button>'
       '<button>Accept</button></div>')


def _page(tmp_path: Path, name: str, extra: str = "", css: str = "") -> Path:
    f = tmp_path / name
    f.write_text(PAGE.format(extra=extra, css=css), encoding="utf-8")
    return f


def _complaints(tmp_path: Path, *items) -> Path:
    folder = tmp_path / ".ux"
    folder.mkdir(exist_ok=True)
    f = folder / "complaints.json"
    f.write_text(json.dumps({"complaints": list(items)}), encoding="utf-8")
    return f


COVER = {"id": "cookie-card", "said": "the cookie banner covers the page",
         "probe": {"kind": "rule-clear", "rule": "first-screen-covered"}}


def _check(*args, **kwargs):
    try:
        return check_complaints(*args, **kwargs)
    except RenderUnavailable as exc:
        pytest.skip(str(exc))


# Reading the complaints.

@pytest.mark.parametrize("item,needle", [
    ({**COVER, "probe": {"kind": "looks-better"}}, "probe.kind is 'looks-better'; write one of"),
    ({**COVER, "said": " "}, ".said is empty; write what the person said"),
    ({**COVER, "id": "Cookie Card"}, ".id is 'Cookie Card'; give it a short id"),
    ({**COVER, "probe": {"kind": "rule-clear", "rule": "prettier"}},
     "probe.rule 'prettier' is no lint or render rule"),
    ({**COVER, "probe": {"kind": "present"}}, "probe.selector is empty; a present probe reads"),
    ({**COVER, "probe": {"kind": "absent", "selector": ".x", "text": "y"}},
     "probe has text, which a absent probe does not read"),
    ({**COVER, "probe": None}, ".probe is missing; add one such as"),
])
def test_every_bad_complaint_names_the_field_and_the_fix(tmp_path, item, needle):
    f = _complaints(tmp_path, item)
    with pytest.raises(InputError) as err:
        load_complaints(f)
    assert needle in str(err.value) and "complaints[0]" in str(err.value)


def test_two_complaints_with_one_id_are_refused(tmp_path):
    f = _complaints(tmp_path, COVER, COVER)
    with pytest.raises(InputError, match=r"complaints\[1\]\.id 'cookie-card' is used twice"):
        load_complaints(f)


def test_a_missing_or_empty_file_says_what_to_write(tmp_path):
    with pytest.raises(InputError, match="does not exist; write the complaints there"):
        load_complaints(tmp_path / "nope.json")
    empty = tmp_path / "empty.json"
    empty.write_text('{"complaints": []}', encoding="utf-8")
    with pytest.raises(InputError, match='has no "complaints" list'):
        load_complaints(empty)


def test_the_page_must_be_html_or_a_url(tmp_path):
    f = _complaints(tmp_path, COVER)
    (tmp_path / "notes.txt").write_text("x", encoding="utf-8")
    with pytest.raises(InputError, match="--page .* is not an HTML file or an http"):
        check_complaints(str(tmp_path / "notes.txt"), file=f)
    with pytest.raises(InputError, match="--page is missing"):
        check_complaints("", file=f)


def test_the_kinds_are_a_closed_list():
    assert set(KINDS) == {"rule-clear", "present", "absent", "text-present", "text-absent"}


# Measuring the page.

def test_the_floating_card_keeps_the_complaint_open_until_it_is_docked(tmp_path):
    f = _complaints(tmp_path, COVER)
    result = _check(str(_page(tmp_path, "card.html", CARD)), file=f)
    assert result["status"] == "open" and result["open"] == ["cookie-card"]
    row = result["complaints"][0]
    assert row["status"] == "open" and "first-screen-covered reported" in row["evidence"]
    assert "cookie-card" in result["message"] and "run the check again" in result["message"]
    fixed = _check(str(_page(tmp_path, "bar.html", BAR)), file=f)
    assert fixed["status"] == "passed" and fixed["open"] == []
    assert fixed["complaints"][0]["status"] == "fixed"


def test_present_must_hold_at_every_width(tmp_path):
    f = _complaints(tmp_path, {"id": "photo", "said": "put a real photo in the hero",
                               "probe": {"kind": "present", "selector": "img.hero"}})
    img = '<img class="hero" alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" ' \
          'style="width:200px;height:120px">'
    hidden_on_phones = "@media (max-width: 500px) { .hero { display: none } }"
    result = _check(str(_page(tmp_path, "p.html", img, hidden_on_phones)), file=f)
    row = result["complaints"][0]
    assert row["status"] == "open" and "390px" in row["evidence"] and "768px" not in row["evidence"]
    assert _check(str(_page(tmp_path, "q.html", img)), file=f)["status"] == "passed"


def test_absent_and_text_probes_read_what_is_visible(tmp_path):
    f = _complaints(
        tmp_path,
        {"id": "no-stars", "said": "drop the fake reviews",
         "probe": {"kind": "absent", "selector": ".stars"}},
        {"id": "no-lorem", "said": "there is still filler text",
         "probe": {"kind": "text-absent", "text": "Lorem   IPSUM"}},
        {"id": "says-local", "said": "say the numbers stay on my device",
         "probe": {"kind": "text-present", "text": "everything stays in your browser"}})
    dirty = '<div class="stars">5 stars</div><p>lorem ipsum dolor</p>'
    result = _check(str(_page(tmp_path, "d.html", dirty)), file=f)
    status = {r["id"]: r["status"] for r in result["complaints"]}
    assert status == {"no-stars": "open", "no-lorem": "open", "says-local": "fixed"}
    hidden = '<div class="stars" style="display:none">5 stars</div>'
    assert _check(str(_page(tmp_path, "c.html", hidden)), file=f)["status"] == "passed"


def test_a_static_lint_rule_can_close_a_complaint(tmp_path):
    f = _complaints(tmp_path, {"id": "filler", "said": "filler text shipped",
                               "probe": {"kind": "rule-clear", "rule": "lorem-ipsum-leak"}})
    assert _check(str(_page(tmp_path, "d.html", "<p>Lorem ipsum dolor sit amet</p>")),
                  file=f)["status"] == "open"
    assert _check(str(_page(tmp_path, "c.html")), file=f)["status"] == "passed"


def test_a_probe_the_old_page_passed_proves_nothing(tmp_path):
    f = _complaints(tmp_path, COVER, {"id": "no-lorem", "said": "filler text",
                                      "probe": {"kind": "text-absent", "text": "lorem"}})
    before = _page(tmp_path, "before.html", CARD)
    result = _check(str(_page(tmp_path, "after.html", BAR)), file=f, before=str(before))
    rows = {r["id"]: r for r in result["complaints"]}
    assert rows["cookie-card"]["status"] == "fixed" and "before" in rows["cookie-card"]
    assert rows["no-lorem"]["status"] == "weak" and "proves nothing" in rows["no-lorem"]["evidence"]
    assert result["status"] == "open" and result["open"] == ["no-lorem"]


def test_a_selector_the_browser_cannot_read_is_named(tmp_path):
    f = _complaints(tmp_path, {"id": "bad", "said": "x",
                               "probe": {"kind": "absent", "selector": "div[[["}})
    with pytest.raises(InputError, match=r"complaint bad: probe.selector 'div\[\[\[' is not a CSS"):
        _check(str(_page(tmp_path, "p.html")), file=f)


def test_a_running_app_is_measured_by_its_url(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    # The card is drawn by a script, so only a page that ran it shows it.
    script = ("<script>document.body.insertAdjacentHTML('beforeend', "
              + json.dumps(CARD) + ")</script>")
    (site / "index.html").write_text(PAGE.format(extra=script, css=""), encoding="utf-8")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler,
                                                           directory=str(site)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        f = _complaints(tmp_path, COVER)
        url = f"http://127.0.0.1:{server.server_address[1]}/index.html"
        result = _check(url, file=f)
    finally:
        server.shutdown()
    assert result["status"] == "open" and result["page"] == url


def test_an_app_that_is_not_running_says_so(tmp_path):
    f = _complaints(tmp_path, COVER)
    with pytest.raises(InputError, match="did not load .*start the app or fix the URL"):
        _check("http://127.0.0.1:9/", file=f)


# The stop hook's gate.

def test_the_gate_reads_the_last_check_without_rendering(tmp_path):
    assert gate(tmp_path) is None  # no complaints, nothing to hold
    f = _complaints(tmp_path, COVER)
    assert "never checked" in gate(tmp_path)
    page = _page(tmp_path, "index.html", CARD)
    _check(str(page), file=f)
    assert "still open" in gate(tmp_path) and "cookie-card" in gate(tmp_path)
    page.write_text(PAGE.format(extra=BAR, css=""), encoding="utf-8")
    assert "changed since the last check" in gate(tmp_path)
    _check(str(page), file=f)
    assert gate(tmp_path) is None
    _complaints(tmp_path, COVER, {**COVER, "id": "another"})
    assert "complaints changed" in gate(tmp_path)


# The command.

def test_the_command_exits_3_while_a_complaint_is_open(tmp_path):
    from click.testing import CliRunner

    from engine.cli.main import cli
    f = _complaints(tmp_path, COVER)
    run = CliRunner().invoke(cli, ["--no-pretty", "complaints", "check", "--file", str(f),
                                   "--page", str(_page(tmp_path, "card.html", CARD))])
    if "No browser" in (run.output or ""):
        pytest.skip(run.output)
    assert run.exit_code == 3, run.output
    assert json.loads(run.stdout)["open"] == ["cookie-card"]
    ok = CliRunner().invoke(cli, ["--no-pretty", "complaints", "check", "--file", str(f),
                                  "--page", str(_page(tmp_path, "bar.html", BAR))])
    assert ok.exit_code == 0, ok.output


# Keeping the page before it changes.

def test_a_snapshot_keeps_the_page_for_before(tmp_path):
    from engine.complaints import snapshot_page
    page = _page(tmp_path, "index.html", CARD)
    out = tmp_path / ".ux" / "before.html"
    assert snapshot_page(str(page), str(out))["status"] == "written"
    assert "We use cookies" in out.read_text(encoding="utf-8")
    assert snapshot_page(str(page), str(out))["status"] == "unchanged"
    page.write_text(PAGE.format(extra=BAR, css=""), encoding="utf-8")
    refused = snapshot_page(str(page), str(out))
    assert refused["status"] == "refused" and "--force" in refused["message"]
    assert "We use cookies" in out.read_text(encoding="utf-8")
    assert snapshot_page(str(page), str(out), force=True)["status"] == "written"
    with pytest.raises(InputError, match="--out .* is a folder; name a file"):
        snapshot_page(str(page), str(tmp_path))


def test_a_snapshot_of_a_url_keeps_what_its_scripts_drew(tmp_path):
    from engine.complaints import snapshot_page
    site = tmp_path / "site"
    site.mkdir()
    script = "<script>document.body.insertAdjacentHTML('beforeend', '<p>drawn</p>')</script>"
    (site / "index.html").write_text(PAGE.format(extra=script, css=""), encoding="utf-8")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler,
                                                           directory=str(site)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    out = tmp_path / "before.html"
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/"
        try:
            snapshot_page(url, str(out))
        except RenderUnavailable as exc:
            pytest.skip(str(exc))
    finally:
        server.shutdown()
    kept = out.read_text(encoding="utf-8")
    assert "<p>drawn</p>" in kept and "<script" not in kept and f'<base href="{url}"' in kept


# What the review found: the snapshot, the gate and the visible text.

def _serve(folder: Path):
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler,
                                                           directory=str(folder)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def test_a_url_that_answers_an_error_is_not_measured(tmp_path):
    f = _complaints(tmp_path, {"id": "promo", "said": "drop the promo",
                               "probe": {"kind": "absent", "selector": ".promo"}})
    server, root = _serve(tmp_path)
    try:
        with pytest.raises(InputError, match="answered HTTP 404"):
            _check(f"{root}/nope/index.html", file=f)
    finally:
        server.shutdown()


def test_a_kept_file_carries_its_styles_so_a_weak_probe_is_caught(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "style.css").write_text(".promo{display:none}", encoding="utf-8")
    page = dist / "index.html"
    page.write_text('<!doctype html><html><head><link rel="stylesheet" href="style.css">'
                    '</head><body><h1>Hi</h1><div class="promo">Sale</div></body></html>',
                    encoding="utf-8")
    from engine.complaints import snapshot_page
    before = tmp_path / ".ux" / "before.html"
    snapshot_page(str(page), str(before))
    (dist / "style.css").write_text(".promo{display:block}", encoding="utf-8")
    kept = before.read_text(encoding="utf-8")
    assert "display: none" in kept and "<link" not in kept
    (dist / "style.css").write_text(".promo{display:none}", encoding="utf-8")
    f = _complaints(tmp_path, {"id": "promo", "said": "drop the promo",
                               "probe": {"kind": "absent", "selector": ".promo"}})
    row = _check(str(page), file=f, before=str(before))["complaints"][0]
    assert row["status"] == "weak"


def test_a_url_keeps_a_relative_base_and_styles_added_by_script(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    (app / "style.css").write_text(".promo{display:none}", encoding="utf-8")
    (app / "index.html").write_text(
        '<!doctype html><html><head><base href="/app/"><link rel="stylesheet" href="style.css">'
        '<style id="s"></style></head><body><h1>Hi</h1><div class="promo">Sale</div>'
        '<div class="cssom">Late</div><script>document.getElementById("s").sheet'
        '.insertRule(".cssom{display:none}")</script></body></html>', encoding="utf-8")
    f = _complaints(tmp_path, {"id": "promo", "said": "x",
                               "probe": {"kind": "absent", "selector": ".promo"}},
                    {"id": "late", "said": "y", "probe": {"kind": "absent", "selector": ".cssom"}})
    server, root = _serve(tmp_path)
    try:
        result = _check(f"{root}/app/index.html", file=f)
    finally:
        server.shutdown()
    assert result["status"] == "passed", result["complaints"]


def test_text_faded_to_nothing_is_not_shown(tmp_path):
    f = _complaints(tmp_path, {"id": "ship", "said": "say shipping is free",
                               "probe": {"kind": "text-present", "text": "free shipping"}})
    faded = '<p style="opacity:0">Free shipping</p>'
    sr_only = ('<span style="position:absolute;width:1px;height:1px;overflow:hidden;'
               'clip:rect(0 0 0 0)">Free shipping</span>')
    assert _check(str(_page(tmp_path, "a.html", faded)), file=f)["status"] == "open"
    assert _check(str(_page(tmp_path, "b.html", sr_only)), file=f)["status"] == "open"
    assert _check(str(_page(tmp_path, "c.html", "<p>Free shipping</p>")),
                  file=f)["status"] == "passed"


def test_the_gate_sees_a_source_edited_after_the_check(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "style.css").write_text("h1{color:#111}", encoding="utf-8")
    page = dist / "index.html"
    page.write_text(PAGE.format(extra='<link rel="stylesheet" href="style.css">' + BAR, css=""),
                    encoding="utf-8")
    f = _complaints(tmp_path, COVER)
    _check(str(page), file=f)
    assert gate(tmp_path) is None
    import os
    import time
    later = time.time() + 5
    os.utime(dist / "style.css", (later, later))
    assert "dist/style.css changed since the last check" in gate(tmp_path)


def test_a_url_check_goes_stale_when_the_app_source_changes(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(PAGE.format(extra=BAR, css=""), encoding="utf-8")
    f = _complaints(tmp_path, COVER)
    server, root = _serve(site)
    try:
        assert _check(f"{root}/index.html", file=f)["status"] == "passed"
    finally:
        server.shutdown()
    assert gate(tmp_path) is None
    import os
    import time
    later = time.time() + 5
    os.utime(site / "index.html", (later, later))
    assert "site/index.html changed since the last check" in gate(tmp_path)

"""Release checks for 4.0, run before a release and by tests/test_release_checks.py.

    python scripts/release_checks.py briefs      # 600 sampled briefs build
    python scripts/release_checks.py roundtrip   # every gallery and fixture system
    python scripts/release_checks.py digest      # stable across PYTHONHASHSEED
    python scripts/release_checks.py wheel       # what the wheel ships

Each check prints one line per failure, naming the input and what differed,
and exits 1 when anything failed.

- briefs: SAMPLES briefs, drawn from a fixed seed over the words the brief
  reader knows, each with its own brand color, build with no failure.
- roundtrip: every system in the gallery (data/gallery) and the fixture
  systems is exported to DTCG, CSS, Tailwind 4 and Figma variables and read
  back by the engine's own importers; every token written is read back
  (every field of a text style included, unless the export names it as one
  it does not write), every token read back stands for one written, and
  each resolves to the value it was written with, in every mode. A gallery
  entry that cannot be built fails the check, naming its file.
- digest: a build's files hash the same under several PYTHONHASHSEED values.
- wheel: a wheel built from a clean copy of the tracked sources holds
  engine/io and engine/foundations and nothing private (no plan, state,
  cache or secret files).
"""
from __future__ import annotations

import functools
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Collection, Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SAMPLES = 600
SEED = 4000
HASH_SEEDS = ("0", "1", "42", "4000")
GALLERY = ROOT / "data" / "gallery"
# Fixture systems: brand and axes the engine's own tests build from.
FIXTURES: Tuple[Tuple[str, Tuple[float, ...]], ...] = (
    ("#3366FF", (0.5,) * 7), ("#FFD400", (0.8, 0.9, 0.2, 0.9, 0.3, 0.9, 0.8)),
    ("#6B4423", (0.2, 0.1, 0.9, 0.1, 0.9, 0.1, 0.1)), ("#808080", (0.0,) * 7),
    ("#0D9488", (1.0,) * 7),
)
# Paths a wheel must hold, and names it must never hold.
WHEEL_NEEDS = ("engine/io/", "engine/foundations/")
WHEEL_FORBIDS = re.compile(r"(?:^|/)(?:PLAN[^/]*\.md|\.ux/|\.uxskill/|\.claude/|\.env|"
                           r"__pycache__/|[^/]*\.pyc|tests/|[^/]*secret[^/]*|[^/]*\.pem)", re.I)


# ---------------------------------------------------------------- briefs


def sample_briefs(n: int = SAMPLES, seed: int = SEED) -> List[Tuple[str, Dict[str, Any]]]:
    """n (brand, brief) pairs drawn from a fixed seed: one to three words
    for each field the brief reader knows, an audience age half the time,
    and a brand color anywhere on the wheel, at any lightness."""
    from engine.foundations.emit import BRIEF_FIELDS, _accepted
    rng = random.Random(seed)
    from engine.foundations.audience import AGES
    ages = sorted(AGES)
    out = []
    for _ in range(n):
        brief: Dict[str, Any] = {}
        for key in BRIEF_FIELDS:
            if rng.random() < 0.7:
                words = list(_accepted(key))
                if key == "industry":
                    brief[key] = rng.choice(words)
                else:
                    brief[key] = rng.sample(words, k=min(len(words), rng.randint(1, 3)))
        if not brief:
            brief["tone"] = [rng.choice(list(_accepted("tone")))]
        if rng.random() < 0.5:
            brief["age"] = rng.choice(ages)
        brand = "#%02X%02X%02X" % tuple(rng.randint(0, 255) for _ in range(3))
        out.append((brand, brief))
    return out


def build_brief(brand: str, brief: Dict[str, Any]) -> List[str]:
    """Problems building one brief; empty when it built and passed."""
    from engine.foundations.emit import brief_audience, choose_axes, make_system
    axes, source = choose_axes(brief, None)
    out = make_system(brand, axes, source, audience=brief_audience(brief))
    if out.passed:
        return []
    return [f"brand {brand} brief {json.dumps(brief, sort_keys=True)}: {f.line()}"
            for f in out.findings]


def check_briefs(pairs: Iterable[Tuple[str, Dict[str, Any]]]) -> List[str]:
    problems: List[str] = []
    for brand, brief in pairs:
        problems.extend(build_brief(brand, brief))
    return problems


# ---------------------------------------------------------------- round trip


def gallery_problems() -> List[str]:
    """Every gallery entry the round trip cannot build, named with the field
    it lacks, so a broken entry fails the check instead of dropping out."""
    problems = []
    for f in sorted(GALLERY.glob("*.json")) if GALLERY.is_dir() else []:
        entry = json.loads(f.read_text(encoding="utf-8"))
        missing = [k for k in ("brand", "axes") if k not in entry]
        if missing:
            problems.append(f"data/gallery/{f.name} has no {' or '.join(missing)}; rebuild it "
                            "with python scripts/build_gallery.py")
    return problems


def labels() -> List[str]:
    """The label of every system the round trip builds: each fixture, then
    each gallery entry gallery_problems does not name."""
    out = [f"fixture {brand}" for brand, _ in FIXTURES]
    for f in sorted(GALLERY.glob("*.json")) if GALLERY.is_dir() else []:
        entry = json.loads(f.read_text(encoding="utf-8"))
        if "brand" in entry and "axes" in entry:
            out.append(f"gallery {f.stem}")
    return out


@functools.lru_cache(maxsize=None)
def system(label: str) -> Any:
    """The token set behind one label from labels(), built once."""
    from engine.foundations import build_system
    from engine.synthesizer.axes import AxisValues
    kind, name = label.split(" ", 1)
    if kind == "fixture":
        axes = dict(FIXTURES)[name]
        return build_system(AxisValues(*axes), name).tokens
    entry = json.loads((GALLERY / f"{name}.json").read_text(encoding="utf-8"))
    return build_system(AxisValues(**entry["axes"]), entry["brand"],
                        arabic=entry.get("arabic", True)).tokens


def systems() -> List[Tuple[str, Any]]:
    """(label, token set) for every gallery system and every fixture."""
    return [(label, system(label)) for label in labels()]


def _flat(value: Any) -> Any:
    """A resolved value in a comparable form: a dimension in px, a
    duration in ms and a number as a number, so a format that writes a
    size as a plain number of pixels compares equal."""
    if isinstance(value, dict) and set(value) == {"value", "unit"}:
        unit = value["unit"]
        factor = 16.0 if unit == "rem" else 1000.0 if unit == "s" else 1.0
        return round(float(value["value"]) * factor, 4)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return round(float(value), 4)
    if isinstance(value, str):
        return value.upper() if value.startswith("#") else value
    if isinstance(value, dict):
        return {k: _flat(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return [_flat(v) for v in value]
    return value


# A text style's fields as a stylesheet or a Figma variable names them one
# by one: --type-text-display-font-size, type.text.display.font-size.
TEXT_FIELDS = {"font-family": "fontFamily", "font-size": "fontSize", "font-weight": "fontWeight",
               "letter-spacing": "letterSpacing", "line-height": "lineHeight"}


def _locate(name: str, written: Any, by_css: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    """The written token (and the text style field, if any) a name read
    back stands for, or (None, None)."""
    path = by_css.get(name, name)
    if written.has(path):
        return path, None
    for kebab, field in TEXT_FIELDS.items():
        for sep in (".", "-"):
            if name.endswith(sep + kebab):
                base = name[:-len(sep + kebab)]
                base = by_css.get(base, base)
                if written.has(base) and written.get(base).type == "typography":
                    return base, field
    return None, None


def _compare(label: str, fmt: str, written: Any, back: Any,
             skipped: Collection[str] = ()) -> Tuple[List[str], int]:
    """Mismatches between the tokens a format wrote and what it read back,
    and the number of values compared. Every token read back must stand for
    a written one (by its path, its custom property name, or one field of a
    text style), and every written token must be read back, every field of
    a text style included, unless the export named it as one it does not
    write (`skipped`). A Figma variable holds one font family, so a family
    stack is compared by its first face (the export says so in its notes)."""
    from engine.foundations.modes import contexts
    from engine.foundations.tokens import css_property
    problems: List[str] = []
    compared = 0
    by_css = {css_property(t.path).lstrip("-"): t.path for t in written.tokens()}
    axes = [a for a in written.axes if a in back.axes]
    seen: Dict[str, set] = {}
    for t in back.tokens():
        path, field = _locate(t.path, written, by_css)
        if path is None:
            problems.append(f"{label} {fmt}: read back {t.path}, which stands for no token the "
                            "export wrote")
            continue
        seen.setdefault(path, set()).add(field)
        family = (field == "fontFamily" or written.get(path).type == "fontFamily") \
            and fmt == "figma"
        for ctx in contexts(tuple(axes), written.axes) or [""]:
            want = written.resolve(path, ctx)
            want = _flat(want[field] if field else want)
            got = _flat(back.resolve(t.path, ctx))
            if family and isinstance(want, list):
                want, got = want[:1], got[:1] if isinstance(got, list) else [got]
            compared += 1
            if want != got:
                where = f"{path}{' ' + field if field else ''}"
                problems.append(f"{label} {fmt}: {where} in {ctx or 'the base'} wrote {want!r} "
                                f"and read back {got!r}")
    for t in written.tokens():
        if t.path in skipped:
            continue
        got = seen.get(t.path)
        if not got:
            problems.append(f"{label} {fmt}: {t.path} was written and nothing was read back for "
                            "it")
        elif None not in got and t.type == "typography":
            lost = sorted(set(written.resolve(t.path)) - got)
            if lost:
                problems.append(f"{label} {fmt}: {t.path} lost {', '.join(lost)} on the way "
                                "back")
    return problems, compared


def round_trip(label: str, ts: Any) -> Tuple[List[str], Dict[str, int]]:
    """Export one system to each format, read it back and compare."""
    from engine.foundations import dump_dtcg, to_css
    from engine.io.css_in import import_css
    from engine.io.dtcg_in import import_dtcg
    from engine.io.figma_in import import_figma
    from engine.io.figma_out import as_export, to_figma
    from engine.io.report import Source
    from engine.io.tailwind_in import import_tailwind_css
    from engine.io.tailwind_out import roles_set as tailwind_roles
    from engine.io.tailwind_out import to_tailwind

    def src(text: str, name: str, fmt: str) -> Source:
        data = text.encode()
        return Source(path=name, format=fmt, sha256=hashlib.sha256(data).hexdigest(),
                      size=len(data))

    figma = to_figma(ts)
    # Each format is compared with what it writes: the system itself, or
    # for Tailwind the roles under their theme names (tailwind_out's own
    # set), and Figma leaves out the tokens its export names as skipped.
    texts = {
        "dtcg": (dump_dtcg(ts), "tokens.json", import_dtcg, ts, ()),
        "css": (to_css(ts), "tokens.css", import_css, ts, ()),
        "tailwind": (to_tailwind(ts, roles=True), "theme.css", import_tailwind_css,
                     tailwind_roles(ts), ()),
        "figma": (json.dumps(as_export(figma)), "variables.json", import_figma, ts,
                  {s["token"] for s in figma.get("skipped", [])}),
    }
    problems: List[str] = []
    counts: Dict[str, int] = {}
    for fmt, (text, name, reader, written, skipped) in texts.items():
        back = reader(text, src(text, name, fmt)).tokens
        found, n = _compare(label, fmt, written, back, skipped)
        problems.extend(found)
        counts[fmt] = n
    return problems, counts


def check_round_trips() -> List[str]:
    problems: List[str] = gallery_problems()
    for label, ts in systems():
        found, counts = round_trip(label, ts)
        problems.extend(found)
        for fmt, n in counts.items():
            if n == 0:
                problems.append(f"{label} {fmt}: nothing was read back to compare")
    return problems


# ---------------------------------------------------------------- digest


_DIGEST_SCRIPT = """
import hashlib, sys
sys.path.insert(0, {root!r})
from engine.foundations.emit import make_system, choose_axes
from engine.synthesizer.axes import AxisValues
h = hashlib.sha256()
for brand in ("#3366FF", "#E11D48", "#808080"):
    out = make_system(brand, AxisValues(0.3, 0.7, 0.4, 0.6, 0.5, 0.8, 0.2), "release check")
    for name in sorted(out.files):
        data = out.files[name]
        h.update(name.encode())
        h.update(data if isinstance(data, bytes) else data.encode())
print(h.hexdigest())
"""


def build_digest(hash_seed: str) -> str:
    env = dict(os.environ, PYTHONHASHSEED=hash_seed)
    run = subprocess.run([sys.executable, "-c", _DIGEST_SCRIPT.format(root=str(ROOT))],
                         capture_output=True, text=True, env=env, check=False)
    if run.returncode != 0:
        raise RuntimeError(f"PYTHONHASHSEED={hash_seed}: the build failed: {run.stderr[-400:]}")
    return run.stdout.strip()


def check_digest(seeds: Sequence[str] = HASH_SEEDS) -> List[str]:
    digests = {s: build_digest(s) for s in seeds}
    if len(set(digests.values())) == 1:
        return []
    return [f"PYTHONHASHSEED={s} gives digest {d}" for s, d in digests.items()]


# ---------------------------------------------------------------- wheel


def wheel_names(wheel: Path) -> List[str]:
    with zipfile.ZipFile(wheel) as z:
        return z.namelist()


def check_wheel_names(names: Sequence[str]) -> List[str]:
    problems = [f"the wheel has nothing under {need}; add it to the package"
                for need in WHEEL_NEEDS if not any(n.startswith(need) for n in names)]
    problems += [f"the wheel ships {n}, which is private or a build leftover; exclude it"
                 for n in names if WHEEL_FORBIDS.search(n)]
    return problems


def tracked_files() -> List[str]:
    """The files git tracks in the checkout (modified ones included), or
    an empty list outside a git checkout."""
    run = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True,
                         check=False)
    if run.returncode != 0:
        return []
    return [n for n in run.stdout.decode().split("\0") if n]


def source_tree(dest: Path) -> Path:
    """A clean copy of the tracked sources in `dest`, so a build never picks
    up a stale build/ folder or an untracked file; the checkout itself
    outside git."""
    names = tracked_files()
    if not names:
        return ROOT
    for name in names:
        src = ROOT / name
        if src.is_file():
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / name)
    return dest


def build_wheel(out: Path) -> Path:
    tree = source_tree(out / "src")
    run = subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation",
                          "-w", str(out), str(tree)], capture_output=True, text=True, check=False)
    if run.returncode != 0:
        raise RuntimeError(f"pip wheel failed: {run.stderr[-600:]}")
    wheels = sorted(out.glob("uxskill-*.whl"))
    if not wheels:
        raise RuntimeError(f"pip wheel wrote no uxskill wheel into {out}")
    return wheels[-1]


def check_wheel() -> List[str]:
    with tempfile.TemporaryDirectory() as tmp:
        return check_wheel_names(wheel_names(build_wheel(Path(tmp))))


CHECKS = {"briefs": lambda: check_briefs(sample_briefs()), "roundtrip": check_round_trips,
          "digest": check_digest, "wheel": check_wheel}


def main(argv: Sequence[str]) -> int:
    names = list(argv) or list(CHECKS)
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        print(f"unknown check {unknown}; run one of {', '.join(CHECKS)}")
        return 2
    failed = 0
    for name in names:
        problems = CHECKS[name]()
        print(f"{name}: {'ok' if not problems else f'{len(problems)} failures'}")
        for p in problems[:50]:
            print(f"  {p}")
        failed += bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

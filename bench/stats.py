"""Wilson intervals, Krippendorff's alpha and the measured tier.

Wilson, for k successes in n with z = 1.96: centre = (p + z^2/2n) / (1 + z^2/n),
half-width = z * sqrt(p(1-p)/n + z^2/4n^2) / (1 + z^2/n). Eval.md Part A uses it.

Krippendorff's alpha, nominal metric, any number of raters per unit and
missing labels allowed: alpha = 1 - D_o / D_e from the coincidence matrix.
When every pairable label is the same value, D_e is zero and alpha is not
defined; ``alpha`` returns None and the report says why.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Z95 = 1.959963984540054

# PLAN-5.0 Principles and eval.md A2.
BLOCKING = (0.95, 0.90)  # precision, Wilson lower bound
ADVISORY = (0.90, 0.75)
INFO = 0.75


def wilson(k: int, n: int, z: float = Z95) -> Tuple[float, float]:
    """The Wilson score interval for k successes in n trials; (0, 1) when n is 0."""
    if n <= 0:
        return 0.0, 1.0
    if k < 0 or k > n:
        raise ValueError(f"k={k} must lie between 0 and n={n}")
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


# A rule is a blocking candidate only when its labelled findings come from at
# least this many distinct pages, since findings on one page are correlated.
MIN_PAGES = 5


def tier(tp: int, fp: int, pages: int = 0) -> str:
    """The tier a rule's labelled findings support. PLAN-5.0 allows blocking at
    precision >= 0.95 with a Wilson lower bound >= 0.90; until usefulness is
    labelled and a person confirms the label sample, the most this returns is
    "blocking-candidate", and only when the findings span at least MIN_PAGES
    pages. Below the floor a rule that meets the bar is "advisory". This is
    what the measurement allows, never a change to the rule's severity."""
    n = tp + fp
    if n == 0:
        return "unmeasured"
    p = tp / n
    lo, _ = wilson(tp, n)
    if p >= BLOCKING[0] and lo >= BLOCKING[1]:
        return "blocking-candidate" if pages >= MIN_PAGES else "advisory"
    if p >= ADVISORY[0] and lo >= ADVISORY[1]:
        return "advisory"
    if p >= INFO:
        return "info"
    return "below-info"


def alpha(units: Iterable[Sequence[Optional[str]]]) -> Optional[float]:
    """Krippendorff's alpha (nominal) over units, each a sequence of labels
    from the raters (None for a missing label). Units with fewer than two
    labels are not pairable and are skipped. None when alpha is undefined."""
    coincid: Counter = Counter()
    for unit in units:
        vals = [v for v in unit if v is not None]
        m = len(vals)
        if m < 2:
            continue
        for i, a in enumerate(vals):
            for j, b in enumerate(vals):
                if i != j:
                    coincid[(a, b)] += 1.0 / (m - 1)
    n_c: Dict[str, float] = Counter()
    for (a, _b), w in coincid.items():
        n_c[a] += w
    n = sum(n_c.values())
    if n <= 1:
        return None
    d_o = sum(w for (a, b), w in coincid.items() if a != b) / n
    d_e = sum(n_c[a] * n_c[b] for a in n_c for b in n_c if a != b) / (n * (n - 1))
    if d_e == 0:
        return None
    return 1.0 - d_o / d_e


def agreement(units: Iterable[Sequence[Optional[str]]]) -> Tuple[int, int]:
    """(units where every label agrees, pairable units)."""
    agree = total = 0
    for unit in units:
        vals = [v for v in unit if v is not None]
        if len(vals) < 2:
            continue
        total += 1
        agree += len(set(vals)) == 1
    return agree, total


def fmt_interval(lo: float, hi: float) -> str:
    return f"{lo:.2f} to {hi:.2f}"


__all__ = [
    "wilson",
    "tier",
    "alpha",
    "agreement",
    "fmt_interval",
    "BLOCKING",
    "ADVISORY",
    "INFO",
    "MIN_PAGES",
    "Z95",
]


def _self_check() -> List[str]:
    """The Part A table of eval.md, recomputed."""
    out = []
    for n, fp, lo in ((35, 0, 0.90), (53, 1, 0.90), (50, 5, 0.79)):
        got = wilson(n - fp, n)[0]
        if round(got, 2) != lo:
            out.append(f"wilson({n - fp},{n}) lower bound {got:.3f}, eval.md says {lo}")
    return out

"""ux-skill v2 — design intelligence engine for AI coding assistants.

Public surface:
    from engine import recommend, lint, discover, generate
    from engine import save_master, save_page, load_master, list_pages
    # v2.1 intelligence loop:
    from engine import synthesize, compute_axes, synthesize_layout
    from engine import compute_type_scale, evaluate, evolve, THRESHOLD
"""

__version__ = "3.1.0"

from engine.persist import save_master, save_page, load_master, list_pages

# v2.1 — intelligence loop public surface
from engine.synthesizer import synthesize, compute_axes
from engine.layout import synthesize_layout
from engine.typography import compute_type_scale
from engine.evaluator import evaluate, THRESHOLD
from engine.evolve import evolve

__all__ = [
    "__version__",
    # v2.0 surface
    "save_master",
    "save_page",
    "load_master",
    "list_pages",
    # v2.1 surface
    "synthesize",
    "compute_axes",
    "synthesize_layout",
    "compute_type_scale",
    "evaluate",
    "THRESHOLD",
    "evolve",
]

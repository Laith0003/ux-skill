"""ux-skill v2 — design intelligence engine for AI coding assistants.

Public surface:
    from engine import recommend, lint, discover, generate
    from engine import save_master, save_page, load_master, list_pages
"""

__version__ = "2.0.0"

from engine.persist import save_master, save_page, load_master, list_pages

__all__ = [
    "__version__",
    "save_master",
    "save_page",
    "load_master",
    "list_pages",
]

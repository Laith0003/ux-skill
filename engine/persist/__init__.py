"""MASTER.md persistence — project-level design system state.

Parity with ui-ux-pro-max's `design-system/MASTER.md` flow. Captures the
current picked style + palette + type + motion + components + brand
exemplars + guardrails as human-readable Markdown so decisions are
version-controllable and survive across sessions.

Public surface
--------------
``save_master(project_root, recommendation, brief) -> str``
``save_page(project_root, page_name, brief, output) -> str``
``load_master(project_root) -> dict | None``
``list_pages(project_root) -> list[str]``
"""
from engine.persist.core import save_master, save_page, load_master, list_pages

__all__ = ["save_master", "save_page", "load_master", "list_pages"]

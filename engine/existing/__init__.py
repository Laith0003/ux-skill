"""An existing design system in a project, found and read, never rewritten.

A project that already has a design system (a DTCG tokens file, a token
build script, CSS custom-property foundation files, a hand-written
MASTER.md or DESIGN.md, a design-system/ or packages/tokens/ folder) is
fixed input. Every command reads it first and none may override,
overwrite or re-derive it. This package finds it and reads the few values
the engine needs (the declared primary, the text color, the font
families, the page language). The full importer is a later milestone.

Public surface
--------------
``detect_existing_system(root) -> dict``
``flatten_dtcg(doc) -> dict``
``is_ux_skill_file(path) -> bool``
``OWNER_KEY``, ``OWNER_VALUE``
"""
from engine.existing.detect import (
    OWNER_KEY, OWNER_VALUE, DESIGN_MD_MARKER, detect_existing_system, flatten_dtcg,
    is_ux_skill_file, css_custom_properties, resolve_css_var, normalize_hex,
)

__all__ = [
    "OWNER_KEY", "OWNER_VALUE", "DESIGN_MD_MARKER", "detect_existing_system",
    "flatten_dtcg", "is_ux_skill_file", "css_custom_properties", "resolve_css_var",
    "normalize_hex",
]

"""An existing design system in a project, found and read, never rewritten.

A project that already has a design system (a DTCG tokens file, a token
build script, CSS custom-property foundation files, a hand-written
MASTER.md or DESIGN.md, a design-system/ or packages/tokens/ folder) is
fixed input. Every command reads it first and none may override,
overwrite or re-derive it. This package finds it and reads the few values
the engine needs (the declared primary, the text color, the font
families, the page language). The full importer is a later milestone.

It also decides who owns a file: ux-skill stamps a digest of its own text
into what it writes, and a file is ux-skill's only while that digest still
matches, so a hand edit makes it the person's file and it is never
overwritten.

Public surface
--------------
``detect_existing_system(root) -> dict``
``flatten_dtcg(doc) -> dict``
``ownership(path) -> str``, ``is_ux_skill_file(path) -> bool``
``stamp_digest(text, comment=False) -> str``
``client_files_in(out_dir, names) -> list``
"""
from engine.existing.detect import (
    DESIGN_MD_MARKER, DIGEST_KEY, OWNER_KEY, OWNER_VALUE, client_files_in,
    css_custom_properties, detect_existing_system, flatten_dtcg, is_ux_skill_file,
    mark_suggestions, normalize_hex, ownership, resolve_css_var, stamp_digest, text_digest,
)

__all__ = [
    "DESIGN_MD_MARKER", "DIGEST_KEY", "OWNER_KEY", "OWNER_VALUE", "client_files_in",
    "css_custom_properties", "detect_existing_system", "flatten_dtcg", "is_ux_skill_file",
    "mark_suggestions", "normalize_hex", "ownership", "resolve_css_var", "stamp_digest", "text_digest",
]

"""Deterministic page-level section-sequence picker.

Picks a whole-page template (from ``data/page-sequences.json``) for a landing
page from the brief's structured fields only. No industry and no word of the
brief's prose picks a sequence: two products in one industry can need
different pages, and any page might say "book" or "payments". The fields
that decide, in order:

``page_sequence`` (a sequence id, wins outright), ``stage`` (pre-launch
picks the pre-launch pattern), ``page`` (feature picks the feature page),
``product_type`` (the engine's one vocabulary, aliases mapped) refined by
``platforms``, ``primary_side`` and ``primary_action``, then
``primary_action`` or ``platforms`` alone, then ``project_type:
mobile-app``. With none of them, ``general-landing``, and ``why`` names the
field to set. ``sign_in: [phone]`` makes the sign-in action a phone field on
whatever sequence is picked.

A section that needs proof names its kind (``stats``, ``testimonials``,
``logos``...). When the brief lists the proof the client has, a section whose
kind is missing is dropped with a stated reason, never filled with invented
proof; a conversion mechanism that needs a missing proof kind or contact route
is dropped the same way.

Pure ``dict -> dict``. No LLM, no network, fully deterministic.

Public surface
--------------
``select_for_brief(brief) -> Dict``: the pick for a 4.0 brief.
``select_sequence(sequence_id) -> Optional[Dict]``: one entry by its id.
``load_sequences() -> List[Dict]``: raw manifest entries.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Mapping, Optional, Tuple

from engine.data_loader import load

PROOF_KINDS: Tuple[str, ...] = ("case-studies", "certifications", "logos", "press", "reviews",
                                "stats", "testimonials")
CONTACT_KINDS: Tuple[str, ...] = ("address", "chat", "email", "form", "phone", "whatsapp")
STAGES: Tuple[str, ...] = ("live", "pre-launch")
PRE_LAUNCH = "pre-launch"
# What the page is for: the product's home, or one feature of it.
PAGES: Tuple[str, ...] = ("home", "feature")
# Where the product runs, and how its users sign in.
PLATFORMS: Tuple[str, ...] = ("web", "ios", "android", "desktop")
STORE_PLATFORMS: Tuple[str, ...] = ("ios", "android")
SIGN_IN: Tuple[str, ...] = ("phone", "email", "password", "sso", "social")
# The side of a two-sided marketplace the page speaks to: demand buys, orders
# or books; supply lists, sells, delivers or hosts.
SIDES: Tuple[str, ...] = ("demand", "supply")
# The one action the page exists for.
ACTIONS: Tuple[str, ...] = ("sign-up", "sign-in", "buy", "quote", "book", "contact", "demo",
                            "download", "subscribe", "open-account")
PROOF_LABELS = {
    "stats": "numbers", "testimonials": "named quotes", "logos": "client logos",
    "reviews": "attributed reviews", "case-studies": "case studies",
    "certifications": "certifications", "press": "press coverage",
}
GENERAL = "general-landing"
FEATURE = "feature-page"
WEB_APP = "web-app"
STORE_APP = "app-mobile-landing"
SUPPLY = "marketplace-supply"
MARKETPLACE = "b2b-marketplace"
SAAS = "saas-marketing"
DEMO = "trust-led"
# The page a product type makes, before its refinements. app is decided by
# platforms; marketing-site (a company with no product) has no page of its own.
BY_PRODUCT: Mapping[str, str] = {
    "marketplace": MARKETPLACE, "commerce": "ecommerce-product",
    "editorial": "content-publication", "local-service": "lead-gen-service", "software": SAAS}
# The page an action makes when the brief names no product type.
BY_ACTION: Mapping[str, str] = {
    "quote": "lead-gen-service", "book": "lead-gen-service", "contact": "lead-gen-service",
    "buy": "ecommerce-product", "subscribe": "content-publication", "demo": DEMO,
    "open-account": MARKETPLACE, "sign-up": SAAS}
_PLATFORMS_FIX = ("set platforms to where it runs (web, ios, android, desktop): a store platform "
                  "gives app-mobile-landing, web without one gives web-app")


def load_sequences() -> List[Dict[str, Any]]:
    """Return the page-sequence entries from the manifest (empty list if absent)."""
    payload = load("page-sequences")
    entries = payload.get("entries", [])
    return entries if isinstance(entries, list) else []


def select_sequence(sequence_id: Any) -> Optional[Dict[str, Any]]:
    """The entry whose id is exactly ``sequence_id`` (case aside), else
    None. Free text never picks a sequence."""
    key = str(sequence_id or "").strip().lower() if isinstance(sequence_id, str) else ""
    return next((e for e in load_sequences() if e["id"] == key), None) if key else None


# ---------------------------------------------------------------- 4.0 briefs


def _fields(brief: Mapping[str, Any]) -> Dict[str, Any]:
    """The brief's fields, from a flat brief or a discovery file's ``answers``."""
    out: Dict[str, Any] = {}
    answers = brief.get("answers")
    if isinstance(answers, Mapping):
        out.update(answers)
    out.update({k: v for k, v in brief.items() if k != "answers"})
    return out


def _choice_list(fields: Mapping[str, Any], name: str,
                 choices: Tuple[str, ...]) -> Optional[List[str]]:
    """A list field from a fixed set, or None when the brief leaves it out.
    ``"none"`` or an empty list means the client has none."""
    if name not in fields or fields[name] is None:
        return None
    value = fields[name]
    if isinstance(value, str):
        value = [] if value.strip().lower() in ("", "none") else [value]
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name}: give a list drawn from {', '.join(choices)}, or [] when the "
                         f"client has none; got {value!r}")
    out: List[str] = []
    for item in value:
        key = "-".join(str(item).strip().lower().split())
        if key not in choices:
            raise ValueError(f"{name}: {item!r} is not one of {', '.join(choices)}; use those "
                             f"words, or [] when the client has none")
        out.append(key)
    return out


def _choice(fields: Mapping[str, Any], name: str, choices: Tuple[str, ...], fix: str) -> str:
    """A one-word field from a fixed set, "" when the brief leaves it out."""
    raw = fields.get(name)
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return ""
    value = "-".join(str(raw).strip().lower().split()) if isinstance(raw, str) else None
    if value not in choices:
        raise ValueError(f"{name}: {raw!r} is not one of {', '.join(choices)}; {fix}")
    return value


def _field_value(fields: Mapping[str, Any], name: str) -> str:
    return "-".join(str(fields.get(name) or "").strip().lower().split())


def product_type_vocabulary() -> Tuple[Tuple[str, ...], Mapping[str, str]]:
    """The one product_type vocabulary the look engine and this picker share
    (engine.foundations.audience), and its alias map."""
    from engine.foundations.audience import PRODUCT_ALIASES, PRODUCT_TYPES
    return tuple(PRODUCT_TYPES), dict(PRODUCT_ALIASES)


def _product_type(fields: Mapping[str, Any]) -> Tuple[str, str]:
    """``(value, written)``: product_type read by the engine's own reader, so
    an alias maps as it does for the system build, and any other value is a
    ValueError naming the field, the values and the aliases."""
    from engine.foundations.audience import AudienceError, product_type_of
    written = _field_value(fields, "product_type")
    if not written:
        return "", ""
    try:
        return product_type_of(fields.get("product_type"), label="brief"), written
    except AudienceError as err:
        raise ValueError(str(err)) from None


class _Brief:
    """The structured fields the picker reads, checked."""

    def __init__(self, fields: Mapping[str, Any]) -> None:
        self.proof = _choice_list(fields, "proof", PROOF_KINDS)
        self.contact = _choice_list(fields, "contact", CONTACT_KINDS)
        self.stage = _choice(fields, "stage", STAGES,
                             "use pre-launch when the product has no customers yet")
        self.product, written = _product_type(fields)
        self.product_label = (f"product_type {self.product}"
                              + (f" (from {written})" if written and written != self.product
                                 else ""))
        self.page = _choice(fields, "page", PAGES, "use feature for a page about one feature of "
                            "the product, home for its main page")
        self.side = _choice(fields, "primary_side", SIDES, "use supply when the page speaks to "
                            "the side that lists, sells, delivers or hosts, demand when it "
                            "speaks to buyers")
        self.action = _choice(fields, "primary_action", ACTIONS, "use the one action the page "
                              "exists for")
        self.platforms = _choice_list(fields, "platforms", PLATFORMS)
        self.sign_in = _choice_list(fields, "sign_in", SIGN_IN)
        self.mobile_project = _field_value(fields, "project_type") == "mobile-app"
        self.industry = _field_value(fields, "industry")

    @property
    def store(self) -> bool:
        return self.platforms is not None and bool(set(self.platforms) & set(STORE_PLATFORMS))

    @property
    def web_only(self) -> bool:
        return self.platforms is not None and "web" in self.platforms and not self.store


def _general(b: _Brief, missing: str) -> Tuple[str, str]:
    note = ("; industry informs the copy and the proof, never the sequence" if b.industry else "")
    return GENERAL, f"general: {missing}{note}"


def _app(b: _Brief, label: str) -> Tuple[str, str]:
    """An app's page follows where it runs."""
    if b.platforms is None:
        if b.mobile_project:
            return STORE_APP, f"{label}; project_type mobile-app: a store app"
        return _general(b, f"{label} needs platforms to pick its sequence; {_PLATFORMS_FIX}")
    listed = ", ".join(b.platforms) or "none"
    if b.store:
        return STORE_APP, f"{label}; platforms {listed}: a store app, so store badges"
    if "web" in b.platforms:
        return WEB_APP, (f"{label}; platforms {listed}: no store app, so the web-app sequence, "
                         f"with no store badges and no download band")
    return _general(b, f"{label}; platforms {listed}: no store and no web page to sign in on, so "
                       f"no store badges; set page_sequence to choose a sequence")


def _live(b: _Brief) -> Tuple[str, str]:
    """The sequence for a live product's page, from its structured fields."""
    if b.side and b.product and b.product != "marketplace":
        raise ValueError(f"primary_side: {b.side!r} names a side of a two-sided marketplace, and "
                         f"{b.product_label} has one side; set product_type to marketplace, or "
                         f"leave primary_side out")
    if b.product == "marketplace" or (b.side and not b.product):
        label = b.product_label if b.product else f"primary_side {b.side}"
        if b.side == "supply":
            return SUPPLY, (f"{label}; primary_side supply: the supply side's path is the primary "
                            f"action and the buyer-only sections drop")
        if b.side == "demand":
            return MARKETPLACE, f"{label}; primary_side demand: the buyer's path leads"
        return MARKETPLACE, (f"{label}: both sides' paths; set primary_side to supply or demand "
                             f"to lead with one")
    if b.product == "app":
        return _app(b, b.product_label)
    if b.product == "software":
        if b.action == "demo":
            return DEMO, f"{b.product_label}; primary_action demo: a demo request leads"
        if b.action == "sign-in" and b.web_only:
            return WEB_APP, (f"{b.product_label}; primary_action sign-in on the web: the web-app "
                             f"sequence")
        if b.store and not b.web_only and b.action == "download":
            return STORE_APP, f"{b.product_label}; primary_action download from a store"
        return SAAS, b.product_label
    if b.product in BY_PRODUCT:
        return BY_PRODUCT[b.product], b.product_label
    if b.product == "marketing-site":
        return _general(b, "product_type marketing-site: a company with no product of its own "
                           "has no sequence of its own; set page_sequence (portfolio-agency for "
                           "a portfolio or an agency)")
    if b.action:
        if b.action in ("sign-in", "download") or (
                b.platforms is not None and b.action not in BY_ACTION):
            return _app(b, f"primary_action {b.action}")
        return BY_ACTION[b.action], f"primary_action {b.action}"
    if b.platforms is not None or b.mobile_project:
        return _app(b, "platforms " + ", ".join(b.platforms or ["from project_type"]))
    return _general(b, "no structured field says what the page is; set product_type (app, "
                       "software, marketing-site, editorial, commerce, marketplace, "
                       "local-service) or primary_action, or page_sequence to choose outright")


def _without_phone(seq: Dict[str, Any], contact: Optional[List[str]]) -> None:
    """Swap in the phone-free text when the brief's contact has no phone, and
    drop the alternates from the result either way."""
    no_phone = contact is not None and "phone" not in contact
    for s in seq["section_sequence"]:
        alt = s.pop("without_phone", None)
        if no_phone and alt:
            s["purpose"] = alt
    for key in ("cta_placement", "footer"):
        alt = seq.pop(f"{key}_without_phone", None)
        if no_phone and alt:
            seq[key] = alt


def _with_phone_sign_in(seq: Dict[str, Any], sign_in: Optional[List[str]]) -> bool:
    """Make every sign-in a phone field when the product signs users in by
    phone: the entry's own phone text where it has one, else a line on the
    hero and the placement. Drops the alternates either way. True when
    applied."""
    phone = sign_in is not None and "phone" in sign_in
    own = False
    for s in seq["section_sequence"]:
        alt = s.pop("with_phone_sign_in", None)
        if phone and alt:
            s["purpose"], own = alt, True
    alt = seq.pop("cta_placement_with_phone_sign_in", None)
    if phone and alt:
        seq["cta_placement"] = alt
    if phone and not own and seq["section_sequence"]:
        hero = seq["section_sequence"][0]
        hero["purpose"] += (" Sign-in is by phone: the account action is one phone number field "
                            "and a continue button, the code step on the next screen, never an "
                            "email field.")
        seq["cta_placement"] += " The header sign-in opens the phone field."
        seq["conversion_mechanisms"] = list(seq.get("conversion_mechanisms") or []) + [
            "phone sign-in"]
    return phone


def _drop_unproven(seq: Dict[str, Any], proof: Optional[List[str]],
                   contact: Optional[List[str]]) -> List[Dict[str, str]]:
    """Remove the sections and mechanisms the client cannot fill; say why."""
    dropped: List[Dict[str, str]] = []
    if proof is not None:
        kept = []
        for s in seq["section_sequence"]:
            kind = s.get("proof")
            if kind and kind not in proof:
                dropped.append({"section": s["section"], "reason": (
                    f"{s['section']} needs the client's real {PROOF_LABELS.get(kind, kind)} "
                    f"(proof: {kind}) and the brief's proof list has none; dropped, never "
                    f"invented.")})
            else:
                kept.append(s)
        seq["section_sequence"] = kept
    needs: Mapping[str, str] = seq.get("mechanism_needs") or {}
    mechanisms = []
    for m in seq.get("conversion_mechanisms") or []:
        need = needs.get(m)
        if need in PROOF_KINDS and proof is not None and need not in proof:
            dropped.append({"mechanism": m, "reason": (
                f"{m} needs the client's real {PROOF_LABELS.get(need, need)} (proof: {need}) "
                f"and the brief's proof list has none; dropped, never invented.")})
        elif need in CONTACT_KINDS and contact is not None and need not in contact:
            listed = ", ".join(contact) or "none"
            dropped.append({"mechanism": m, "reason": (
                f"{m} needs a {need} route and the brief's contact list has {listed}; dropped, "
                f"never invented.")})
        else:
            mechanisms.append(m)
    seq["conversion_mechanisms"] = mechanisms
    return dropped


def select_for_brief(brief: Mapping[str, Any]) -> Dict[str, Any]:
    """Pick the page sequence for a 4.0 brief, and say why. Always returns one.

    Reads a flat brief (``.ux/system-brief.json``, the MCP ``brief`` object) or
    a discovery file (``{"answers": {...}}``). Only structured fields decide
    (see the module docstring); ``industry`` and the brief's prose never do.
    When a field the pick needs is missing, the result is ``general-landing``
    and ``why`` names that field and how to set it.

    ``proof`` (from PROOF_KINDS, ``[]`` for none) and ``contact`` (from
    CONTACT_KINDS) drop what the client cannot back, each with a reason; with
    ``proof`` left out, proof sections stay, marked by kind, and
    ``proof_unknown`` is true. A field outside its choices raises
    ``ValueError`` naming the field and the choices.
    """
    b = _Brief(_fields(brief or {}))
    entries = load_sequences()
    by_id = {e["id"]: e for e in entries}
    explicit = str(_fields(brief or {}).get("page_sequence") or "").strip()
    dropped: List[Dict[str, str]] = []
    if explicit:
        if explicit not in by_id:
            raise ValueError(f"page_sequence: {explicit!r} is not a sequence; use one of "
                             f"{', '.join(sorted(by_id))}")
        sid, why = explicit, f"page_sequence {explicit}"
    elif b.stage == PRE_LAUNCH:
        live_id, _ = _live(b)
        live = by_id[live_id]
        sid, why = PRE_LAUNCH, f"stage pre-launch; the live pick would be {live_id}"
        proof_sections = [s["section"] for s in live.get("section_sequence", []) if s.get("proof")]
        reason = ("the product has not launched, so the client has no {} yet; the page states "
                  "what exists instead of inventing it.")
        dropped = ([{"section": name, "reason": f"{name}: " + reason.format("proof of this kind")}
                    for name in proof_sections]
                   or [{"section": "Proof", "reason": "Proof: " + reason.format("proof")}])
        if b.proof:
            dropped.append({"section": "Proof", "reason": (
                f"The brief lists proof ({', '.join(b.proof)}) with stage pre-launch. If that "
                f"proof is real, set stage to live: {live_id} shows it in its proof sections. The "
                f"pre-launch pattern shows none.")})
    elif b.page == "feature":
        sid = FEATURE
        why = ("page feature: a page about one feature of a product people already use, so no "
               "founding team and no early-access form")
        if b.side:
            why += (f"; primary_side {b.side} is not read on a feature page, which speaks to the "
                    f"feature's users")
    else:
        sid, why = _live(b)

    seq = copy.deepcopy(by_id[sid])
    seq.pop("picked_by", None)
    _without_phone(seq, b.contact)
    if _with_phone_sign_in(seq, b.sign_in):
        why += "; sign_in phone: every sign-in is a phone number field"
    if seq["id"] != PRE_LAUNCH:
        dropped += _drop_unproven(seq, b.proof, b.contact)
    seq["why"] = why
    seq["dropped"] = dropped
    seq["proof_unknown"] = b.proof is None and any(s.get("proof") for s in seq["section_sequence"])
    return seq

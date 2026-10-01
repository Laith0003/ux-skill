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

Every section names its job (ask, proof, objection, explanation or
navigation). Three fields shape the page around its ask without changing the
pick: ``commitment`` (what the visitor gives; a heavy one is repeated only
below a section that answers an objection or shows proof), ``arrival`` (what
the visitor knows on landing; branded drops the case for the category, cold
with a heavy ask adds a lighter step as a text link) and ``objections`` (the
customer's own words, typed, each placed in the section that answers it).
``page: campaign`` closes the page's exits. Every change is reported in
``why`` or ``dropped``.

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
# What the page is for: the product's home, one feature of it, one campaign
# whose only job is one ask, or an inner page of the site.
PAGES: Tuple[str, ...] = ("home", "feature", "campaign", "pricing", "about", "contact",
                          "customers", "customer-story", "legal")
# Inner pages and the sequence each picks. They open on a secondary hero and
# share the site's header, closing band and footer (one page family).
INNER_PAGES: Dict[str, str] = {"pricing": "pricing-page", "about": "about-page",
                               "contact": "contact-page", "customers": "customers-page",
                               "customer-story": "customer-story", "legal": "legal-page"}
# What the visitor gives at the ask. The last four are heavy: card details, a
# call, a purchase or a signed contract need their objections answered above
# the first place the ask is repeated.
COMMITMENTS: Tuple[str, ...] = ("email", "phone", "account", "trial", "card", "call",
                                "purchase", "contract")
HEAVY_COMMITMENTS: Tuple[str, ...] = ("card", "call", "purchase", "contract")
# What the visitor knows on landing.
ARRIVALS: Tuple[str, ...] = ("cold", "warm", "branded", "returning")
# The kinds of objection a customer raises; approval is the reader who is not
# the buyer and needs something to take to whoever approves.
OBJECTION_TYPES: Tuple[str, ...] = ("function", "risk", "price", "payback", "timing",
                                    "approval")
# What each section does for the ask.
JOBS: Tuple[str, ...] = ("ask", "proof", "objection", "explanation", "navigation")
# What a visitor needs answered next to the ask, growing with the commitment.
_AT_THE_ASK_LIGHT: Tuple[str, ...] = (
    "what happens next, and when",
    "what happens to the data the visitor gives")
_AT_THE_ASK_ACCOUNT: Tuple[str, ...] = (
    "what it costs later, and how to cancel or close it",)
_AT_THE_ASK_HEAVY: Tuple[str, ...] = (
    "who runs this: the legal name and a way to reach them",
    "what happens if it goes wrong: the refund, cancellation or guarantee terms")
OBJECTION_SECTION = "FAQ (objections)"
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
# The page an action makes when the brief names no product type. No action
# alone makes a two-sided marketplace: that needs its sides in the brief.
BY_ACTION: Mapping[str, str] = {
    "quote": "lead-gen-service", "book": "lead-gen-service", "contact": "lead-gen-service",
    "buy": "ecommerce-product", "subscribe": "content-publication", "demo": DEMO,
    "sign-up": SAAS}
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


def _objections(fields: Mapping[str, Any]) -> List[Dict[str, str]]:
    """The customer's objections, each ``{quote, type, source}``, checked. The
    quote is kept exactly as given: it is the customer's wording."""
    raw = fields.get("objections")
    if raw is None:
        return []
    shape = ("give a list of {quote, type, source} objects, one per objection in the "
             "customer's own words, or leave it out")
    if not isinstance(raw, (list, tuple)):
        raise ValueError(f"objections: {shape}; got {raw!r}")
    out: List[Dict[str, str]] = []
    for i, item in enumerate(raw):
        at = f"objections[{i}]"
        if not isinstance(item, Mapping):
            raise ValueError(f"{at}: give an object with quote, type and source; got {item!r}")
        quote = item.get("quote")
        if quote is not None and not isinstance(quote, str):
            raise ValueError(f"{at}.quote: give the customer's words as text; got {quote!r}")
        if not isinstance(quote, str) or not quote.strip():
            raise ValueError(f"{at}.quote: paste the customer's own words (a review, a call "
                             f"note, a support ticket); it is empty")
        kind = "-".join(str(item.get("type") or "").strip().lower().split())
        if kind not in OBJECTION_TYPES:
            raise ValueError(f"{at}.type: {item.get('type')!r} is not one of "
                             f"{', '.join(OBJECTION_TYPES)}; use approval when the reader is "
                             f"not the one who approves the purchase")
        source = item.get("source")
        if source is not None and not isinstance(source, str):
            raise ValueError(f"{at}.source: name where the words come from, as text; got "
                             f"{source!r}")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"{at}.source: name where the words come from (a review, a sales "
                             f"call, a support ticket, a comment); it is empty")
        out.append({"quote": quote, "type": kind, "source": source.strip()})
    return out


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
                            "the product, campaign for a page whose only job is one ask, home "
                            "for its main page, or the inner page it is (pricing, about, "
                            "contact, customers, customer-story, legal)")
        self.commitment = _choice(fields, "commitment", COMMITMENTS, "name what the visitor "
                                  "gives at the ask, or leave it out")
        self.arrival = _choice(fields, "arrival", ARRIVALS, "name what most visitors know on "
                               "landing, or leave it out")
        self.objections = _objections(fields)
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
    if b.action == "open-account":
        return _general(b, "primary_action open-account needs product_type: marketplace for a "
                           "trade account on a two-sided market (with primary_side), app or "
                           "software for a bank, a wallet or a broker")
    if b.action:
        if b.action in ("sign-in", "download") or (
                b.platforms is not None and b.action not in BY_ACTION):
            return _app(b, f"primary_action {b.action}")
        why = f"primary_action {b.action}"
        if b.platforms is not None:
            listed = ", ".join(b.platforms) or "none"
            why += (f"; platforms {listed} not read without product_type: set product_type "
                    f"app to let platforms pick")
        return BY_ACTION[b.action], why
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
    if contact is not None:
        kept = []
        for s in seq["section_sequence"]:
            need = s.get("contact")
            if need and need not in contact:
                listed = ", ".join(contact) or "none"
                dropped.append({"section": s["section"], "reason": (
                    f"{s['section']} needs a {need} route (contact: {need}) and the brief's "
                    f"contact list has {listed}; dropped, never invented. Add {need} to contact "
                    f"if the client has one.")})
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


def _drop_pre_launch_proof(seq: Dict[str, Any], proof: Optional[List[str]]) -> List[Dict[str, str]]:
    """An inner page before launch: remove every proof section and mechanism,
    with the pre-launch reason, and point a brief that lists proof at stage."""
    reason = ("the product has not launched, so the client has no {} yet; the page states "
              "what exists instead of inventing it.")
    dropped = [{"section": s["section"], "reason": f"{s['section']}: " + reason.format(
        PROOF_LABELS.get(s["proof"], s["proof"]))}
        for s in seq["section_sequence"] if s.get("proof")]
    seq["section_sequence"] = [s for s in seq["section_sequence"] if not s.get("proof")]
    needs: Mapping[str, str] = seq.get("mechanism_needs") or {}
    for m in [m for m in seq.get("conversion_mechanisms") or [] if needs.get(m) in PROOF_KINDS]:
        dropped.append({"mechanism": m, "reason": f"{m}: " + reason.format(
            PROOF_LABELS.get(needs[m], needs[m]))})
    seq["conversion_mechanisms"] = [m for m in seq.get("conversion_mechanisms") or []
                                    if needs.get(m) not in PROOF_KINDS]
    if proof:
        dropped.append({"section": "Proof", "reason": (
            f"The brief lists proof ({', '.join(proof)}) with stage pre-launch. If that proof is "
            f"real, set stage to live to show it; before launch the page shows none.")})
    return dropped


def _closing_ask(secs: List[Dict[str, Any]]) -> int:
    """Index of the closing ask band: the last ask before the footer."""
    return max(i for i, s in enumerate(secs) if s["job"] == "ask")


def _objection_section(seq: Dict[str, Any], notes: List[str]) -> int:
    """Index of the page's FAQ, else of a new FAQ inserted before the closing
    band (reported once in ``notes``)."""
    secs = seq["section_sequence"]
    for i, s in enumerate(secs):
        if s["job"] == "objection" and s["section"].startswith("FAQ"):
            return i
    at = _closing_ask(secs)
    secs.insert(at, {"section": OBJECTION_SECTION, "job": "objection", "purpose": (
        "The objections that stop the action, answered above the closing band. Its questions "
        "come from the brief's objections, each in the customer's own words turned into a "
        "question; with no objections in the brief, it answers only the operational questions "
        "the client's own material answers: price, delivery, what happens next.")})
    notes.append(f"{OBJECTION_SECTION} added before {secs[at + 1]['section']}: nothing else on "
                 f"the page answers the objections in the brief")
    return at


def _place_the_ask(seq: Dict[str, Any], b: _Brief, dropped: List[Dict[str, str]]) -> List[str]:
    """Shape the page around what the visitor gives at the ask and what they
    know on landing. Returns the notes for ``why``; drops go to ``dropped``."""
    notes: List[str] = []
    secs = seq["section_sequence"]
    if b.arrival == "branded":
        for s in [s for s in secs if s.get("explains_category")]:
            secs.remove(s)
            dropped.append({"section": s["section"], "reason": (
                f"{s['section']} argues for the category, and with arrival branded the visitor "
                f"searched the brand's name and knows what it is; dropped.")})
            notes.append(f"arrival branded: dropped {s['section']}")
    if b.commitment and b.commitment not in HEAVY_COMMITMENTS:
        notes.append(f"commitment {b.commitment}: a light ask, so it stays in the hero")
    elif b.commitment:
        heavy = f"commitment {b.commitment}: a heavy ask"
        answers = [i for i, s in enumerate(secs) if i > 0 and s["job"] in ("proof", "objection")]
        first = answers[0] if answers else _objection_section(seq, notes)
        while True:
            repeat = next(i for i, s in enumerate(secs) if i > 0 and s["job"] == "ask")
            if repeat > first:
                break
            moved = secs.pop(repeat)
            first -= 1
            secs.insert(first + 1, moved)
            heavy += f"; moved {moved['section']} below {secs[first]['section']}"
        if secs[first + 1]["job"] != "ask":
            secs.insert(first + 1, {"section": "Mid-page ask", "job": "ask", "purpose": (
                "The primary action again, with the hero's verb, right after the first section "
                "that answers an objection or shows proof: the visitor who has read that far "
                "can act without scrolling back.")})
            heavy += (f"; Mid-page ask after {secs[first]['section']}, the first section that "
                      f"answers an objection or shows proof")
        notes.append(heavy)
        seq["cta_placement"] += (" The ask is heavy: the hero's action says what it takes, and "
                                 "it is repeated only below a section that answers an "
                                 "objection or shows proof.")
        if b.arrival == "cold":
            seq["cta_placement"] += (
                " Most visitors arrive cold: a lighter step the client really offers (a price "
                "list, a sample, a recorded demo, a question by a contact route) sits beside "
                "the primary action as a text link, never a second button; with none, leave "
                "it out and list it for the owner.")
            seq["conversion_mechanisms"] = list(seq.get("conversion_mechanisms") or []) + [
                "lighter step (text link)"]
            notes.append("arrival cold with a heavy ask: a lighter step as a text link")
    return notes


def _at_the_ask(commitment: str) -> List[str]:
    """What the page answers next to the form or payment field."""
    if not commitment:
        return []
    out = list(_AT_THE_ASK_LIGHT)
    if commitment in ("account", "trial") or commitment in HEAVY_COMMITMENTS:
        out += _AT_THE_ASK_ACCOUNT
    if commitment in HEAVY_COMMITMENTS:
        out += _AT_THE_ASK_HEAVY
    return out


def _map_objections(seq: Dict[str, Any], objections: List[Dict[str, str]],
                    notes: List[str]) -> List[Dict[str, str]]:
    """Place each objection in the section that answers it: function in the
    page's how-it-works section, price in its pricing section, payback next to
    its first proof, everything else (and any type with no such section) in
    its FAQ."""
    out: List[Dict[str, str]] = []
    for o in objections:
        secs = seq["section_sequence"]
        target: Optional[Dict[str, Any]] = None
        if o["type"] == "function":
            target = next((s for s in secs if s["job"] == "explanation"
                           and s["section"].startswith("How ")), None)
        elif o["type"] == "price":
            target = next((s for s in secs if "pricing" in s["section"].lower()), None)
        elif o["type"] == "payback":
            target = next((s for s in secs if s["job"] == "proof"), None)
        if target is None:
            target = secs[_objection_section(seq, notes)]
        out.append({**o, "section": target["section"]})
    return out


def _campaign(seq: Dict[str, Any]) -> None:
    """A campaign page closes its exits: logo and one action in the header, a
    footer with the legal links and the contact routes only."""
    foot = seq["section_sequence"][-1]
    foot["section"] = "Compact footer"
    foot["purpose"] = ("A reduced footer: the legal links and the contact routes the client "
                       "offers, nothing else; no link columns and no social row.")
    seq["footer"] = "Compact footer: legal links and the contact routes the client offers."
    seq["cta_placement"] += (" A campaign page: the header holds the logo and the one primary "
                             "action, no nav links; a link out from a proof item opens in a new "
                             "tab and says so.")


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

    ``objection_map`` lists each objection with the section that answers it;
    ``at_the_ask`` lists what the page answers next to the form or payment
    field for the brief's ``commitment`` (empty without one).
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
    elif b.page in INNER_PAGES:
        sid = INNER_PAGES[b.page]
        why = (f"page {b.page}: an inner page of the site, opened by a secondary hero that names "
               f"the page, and sharing the site's header, closing band and footer")
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
    if b.page in INNER_PAGES and b.stage == PRE_LAUNCH and not explicit:
        why += "; stage pre-launch: the page shows no proof, since the product has not launched"
        dropped += _drop_pre_launch_proof(seq, b.proof)
    if seq["id"] != PRE_LAUNCH:
        dropped += _drop_unproven(seq, b.proof, b.contact)
    if b.page == "campaign":
        _campaign(seq)
        why += ("; page campaign: one ask, so the header drops its links and the footer keeps "
                "the legal links and contact routes only")
    notes = _place_the_ask(seq, b, dropped)
    seq["objection_map"] = _map_objections(seq, b.objections, notes)
    seq["at_the_ask"] = _at_the_ask(b.commitment)
    why += "".join("; " + n for n in notes)
    seq["why"] = why
    seq["dropped"] = dropped
    seq["proof_unknown"] = b.proof is None and any(s.get("proof") for s in seq["section_sequence"])
    return seq

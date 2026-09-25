"""Deterministic page-level section-sequence picker.

Picks a whole-page template (from ``data/page-sequences.json``) for a landing
page. ``select_for_brief`` reads a 4.0 brief in tiers: an explicit
``page_sequence``, then ``stage``, then ``product_type``, ``project_type`` and
``industry``, then the brief's own phrases, and ``general-landing`` when
nothing points elsewhere, so it always returns a sequence. ``select_sequence``
scores free text alone. A call-to-action verb ("book", "buy", "download")
never picks a sequence: any page might say it.

A section that needs proof names its kind (``stats``, ``testimonials``,
``logos``...). When the brief lists the proof the client has, a section whose
kind is missing is dropped with a stated reason, never filled with invented
proof; a conversion mechanism that needs a missing proof kind or contact route
is dropped the same way.

Pure ``dict -> dict``. No LLM, no network, fully deterministic: the same brief
always returns the same sequence, and ties are broken by manifest order.

Public surface
--------------
``select_for_brief(brief) -> Dict``: the pick for a 4.0 brief.
``select_sequence(goal_or_keywords) -> Optional[Dict]``: best match for free text.
``score_sequence(entry, tokens, raw) -> float``: the text score (exposed for tests).
``load_sequences() -> List[Dict]``: raw manifest entries.
"""
from __future__ import annotations

import copy
import re
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union

from engine.data_loader import load


_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Words a call to action or a sentence uses on any page. They never count as a
# match on their own, so a brief that says "book a demo" is not a booking page.
CTA_VERBS = frozenset({
    "book", "booking", "buy", "call", "contact", "download", "get", "hire", "install", "join",
    "learn", "order", "request", "shop", "sign", "start", "subscribe", "try", "see", "open",
})
STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it", "its",
    "me", "my", "now", "of", "on", "or", "our", "the", "their", "them", "to", "today", "up",
    "us", "we", "who", "with", "you", "your", "can", "will", "that", "this", "all", "more",
})
PROOF_KINDS: Tuple[str, ...] = ("case-studies", "certifications", "logos", "press", "reviews",
                                "stats", "testimonials")
CONTACT_KINDS: Tuple[str, ...] = ("address", "chat", "email", "form", "phone", "whatsapp")
STAGES: Tuple[str, ...] = ("live", "pre-launch")
PRE_LAUNCH = "pre-launch"
PROOF_LABELS = {
    "stats": "numbers", "testimonials": "named quotes", "logos": "client logos",
    "reviews": "attributed reviews", "case-studies": "case studies",
    "certifications": "certifications", "press": "press coverage",
}
GENERAL = "general-landing"
# Plain text fields read for phrases. Tone words and must-haves shape the look,
# not the page's sections, and the structured fields decide in their own tiers,
# so none of them is read again as a phrase.
TEXT_FIELDS = ("goal", "primary_goal", "audience", "description", "product", "summary", "offer")


def load_sequences() -> List[Dict[str, Any]]:
    """Return the page-sequence entries from the manifest (empty list if absent)."""
    payload = load("page-sequences")
    entries = payload.get("entries", [])
    return entries if isinstance(entries, list) else []


def _tokenize(text: str) -> List[str]:
    """Lowercase word/number tokens from arbitrary text."""
    return _TOKEN_RE.findall((text or "").lower())


def _content(tokens: Iterable[str]) -> set:
    """Tokens that can carry a match: no stop words, no call-to-action verbs."""
    return {t for t in tokens if t not in STOP_WORDS and t not in CTA_VERBS}


def _normalize_query(goal_or_keywords: Union[str, List[str], None]):
    """Return ``(raw_lower, token_set)`` for a string or list-of-strings query."""
    if goal_or_keywords is None:
        return "", set()
    if isinstance(goal_or_keywords, (list, tuple)):
        raw = " ".join(str(x) for x in goal_or_keywords)
    else:
        raw = str(goal_or_keywords)
    raw_lower = " ".join(raw.strip().lower().split())
    return raw_lower, set(_tokenize(raw_lower))


def _phrase_in(phrase: str, raw: str) -> bool:
    """True when ``phrase`` appears in ``raw`` as whole words."""
    return bool(re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", raw))


def score_sequence(entry: Dict[str, Any], query_tokens: set, raw_query: str) -> float:
    """Score one entry against a normalized query. Higher is a better match.

    Signal (additive, deterministic):
      * exact goal/id match                        -> strong base (100)
      * goal id appears in the query as words      -> (50)
      * a keyword phrase appears as whole words    -> +6 per phrase
      * shared content tokens (no stop words and   -> +2 per token
        no call-to-action verbs)
    """
    goal = str(entry.get("goal") or entry.get("id") or "").strip().lower()
    keywords = [str(k).strip().lower() for k in (entry.get("keywords") or [])]

    score = 0.0
    if goal and (goal == raw_query or goal in query_tokens):
        score += 100.0
    elif goal and raw_query and _phrase_in(goal, raw_query):
        score += 50.0

    for kw in keywords:
        if kw and raw_query and _content(_tokenize(kw)) and _phrase_in(kw, raw_query):
            score += 6.0

    entry_tokens: set = set()
    for kw in keywords:
        entry_tokens.update(_tokenize(kw))
    entry_tokens.update(_tokenize(goal))
    score += 2.0 * len(_content(query_tokens) & _content(entry_tokens))
    return score


def select_sequence(goal_or_keywords: Union[str, List[str], None]) -> Optional[Dict[str, Any]]:
    """Return the best-matching page sequence for a goal id or a free-text brief.

    Deterministic: entries are scored, the highest score wins, and ties are broken
    by manifest order (first defined wins). Returns ``None`` when there are no
    entries or nothing scores above zero (no signal, no opinion).
    """
    entries = load_sequences()
    raw_query, query_tokens = _normalize_query(goal_or_keywords)
    if not entries or not raw_query:
        return None
    best: Optional[Dict[str, Any]] = None
    best_score = 0.0
    for entry in entries:
        s = score_sequence(entry, query_tokens, raw_query)
        if s > best_score:
            best_score, best = s, entry
    return best if best_score > 0 else None


# ---------------------------------------------------------------- 4.0 briefs


def _fields(brief: Mapping[str, Any]) -> Dict[str, Any]:
    """The brief's fields, from a flat brief or a discovery file's ``answers``."""
    out: Dict[str, Any] = {}
    answers = brief.get("answers")
    if isinstance(answers, Mapping):
        out.update(answers)
    out.update({k: v for k, v in brief.items() if k != "answers"})
    return out


def _text(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return " ".join(_text(v) for v in value)
    if isinstance(value, Mapping):
        return " ".join(_text(v) for v in value.values())
    return str(value) if value is not None else ""


def _choice_list(fields: Mapping[str, Any], name: str, choices: Tuple[str, ...]) -> Optional[List[str]]:
    """A list field from a fixed set, or None when the brief leaves it out.
    ``"none"`` or an empty list means the client has none."""
    if name not in fields or fields[name] is None:
        return None
    value = fields[name]
    if isinstance(value, str):
        value = [] if value.strip().lower() in ("", "none") else [value]
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name}: give a list drawn from {', '.join(choices)}, or [] when the client "
                         f"has none; got {value!r}")
    out: List[str] = []
    for item in value:
        key = str(item).strip().lower()
        if key not in choices:
            raise ValueError(f"{name}: {item!r} is not one of {', '.join(choices)}; use those words, or "
                             f"[] when the client has none")
        out.append(key)
    return out


def _field_value(fields: Mapping[str, Any], name: str) -> str:
    return "-".join(str(fields.get(name) or "").strip().lower().split())


def _industry(fields: Mapping[str, Any]) -> str:
    """The brief's industry as the look engine reads it: its other names
    (building-materials, wholesale...) resolve to the seeded id."""
    from engine.synthesizer.axes import INDUSTRY_ALIASES
    value = _field_value(fields, "industry")
    return INDUSTRY_ALIASES.get(value, value)


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


def _phrases(entry: Mapping[str, Any], raw: str) -> List[str]:
    return [k for k in entry.get("keywords") or []
            if _content(_tokenize(k)) and _phrase_in(k.lower(), raw)]


def _best(entries: List[Dict[str, Any]], fields: Mapping[str, Any]) -> Tuple[Dict[str, Any], str]:
    """Pick in tiers: product_type narrows the entries, then project_type,
    then industry; the brief's phrases choose among what is left. With no
    phrase, the first entry that lists the product_type first wins, then
    manifest order. With nothing to go on, general-landing."""
    live = [e for e in entries if e["id"] not in (PRE_LAUNCH, GENERAL)]
    cands, why = live, []
    pt, written = _product_type(fields)
    tiers = (("product_type", pt, "product_types"),
             ("project_type", _field_value(fields, "project_type"), "project_types"),
             ("industry", _industry(fields), "industries"))
    for name, value, key in tiers:
        if not value:
            continue
        narrowed = [e for e in cands if value in (e.get(key) or [])]
        if narrowed:
            label = f"{name} {value}"
            if name == "product_type" and written != value:
                label += f" (from {written})"
            cands, why = narrowed, why + [label]
    raw, tokens = _normalize_query(" ".join(_text(fields.get(f)) for f in TEXT_FIELDS).replace("-", " "))
    best, best_score = None, 0.0
    if raw:
        for entry in cands:
            s = score_sequence(entry, tokens, raw)
            if s > best_score:
                best, best_score = entry, s
    if best is not None:
        phrases = _phrases(best, raw)
        why.append(f"phrases {', '.join(phrases[:4])}" if phrases else "shared words in the brief")
        return best, "; ".join(why)
    if why:
        rank = {e["id"]: i for i, e in enumerate(cands)}
        pick = min(cands, key=lambda e: ((e.get("product_types") or [pt]).index(pt)
                                         if pt in (e.get("product_types") or []) else 9, rank[e["id"]]))
        return pick, "; ".join(why)
    general = next(e for e in entries if e["id"] == GENERAL)
    return general, ("general: no field or phrase in the brief points to a specific sequence, so the "
                     "general landing sequence; set page_sequence to choose another")


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
                    f"{s['section']} needs the client's real {PROOF_LABELS.get(kind, kind)} (proof: {kind}) "
                    f"and the brief's proof list has none; dropped, never invented.")})
            else:
                kept.append(s)
        seq["section_sequence"] = kept
    needs: Mapping[str, str] = seq.get("mechanism_needs") or {}
    mechanisms = []
    for m in seq.get("conversion_mechanisms") or []:
        need = needs.get(m)
        if need in PROOF_KINDS and proof is not None and need not in proof:
            dropped.append({"mechanism": m, "reason": (
                f"{m} needs the client's real {PROOF_LABELS.get(need, need)} (proof: {need}) and the "
                f"brief's proof list has none; dropped, never invented.")})
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
    a discovery file (``{"answers": {...}}``). In order:

    1. ``page_sequence``: a sequence id; wins outright.
    2. ``stage``: ``live`` or ``pre-launch``; pre-launch picks the honest
       pre-launch pattern, which has no proof section.
    3. ``product_type`` (the look engine's list: app, software,
       marketing-site, editorial, commerce), then ``project_type``, then
       ``industry`` (the /ux-system list, or one of its other names): each
       narrows the entries that list it.
    4. The brief's own phrases choose among what is left.
    5. With nothing to go on, ``general-landing``.

    ``proof`` (from PROOF_KINDS, ``[]`` for none) and ``contact`` (from
    CONTACT_KINDS) drop what the client cannot back, each with a reason; with
    ``proof`` left out, proof sections stay, marked by kind, and
    ``proof_unknown`` is true. A field outside its choices raises
    ``ValueError`` naming the field and the choices.
    """
    fields = _fields(brief or {})
    entries = load_sequences()
    by_id = {e["id"]: e for e in entries}
    proof = _choice_list(fields, "proof", PROOF_KINDS)
    contact = _choice_list(fields, "contact", CONTACT_KINDS)
    stage = str(fields.get("stage") or "").strip().lower()
    if stage and stage not in STAGES:
        raise ValueError(f"stage: {fields.get('stage')!r} is not one of {', '.join(STAGES)}; use "
                         f"pre-launch when the product has no customers yet")
    _product_type(fields)

    explicit = str(fields.get("page_sequence") or "").strip()
    dropped: List[Dict[str, str]] = []
    if explicit:
        if explicit not in by_id:
            raise ValueError(f"page_sequence: {explicit!r} is not a sequence; use one of "
                             f"{', '.join(sorted(by_id))}")
        entry, why = by_id[explicit], f"page_sequence {explicit}"
    elif stage == PRE_LAUNCH and PRE_LAUNCH in by_id:
        entry = by_id[PRE_LAUNCH]
        live, _ = _best(entries, fields)
        proof_sections = [s["section"] for s in live.get("section_sequence", []) if s.get("proof")]
        why = f"stage pre-launch; the live pick would be {live['id']}"
        reason = ("the product has not launched, so the client has no {} yet; the page states what exists "
                  "instead of inventing it.")
        dropped = [{"section": name, "reason": f"{name}: " + reason.format("proof of this kind")}
                   for name in proof_sections] or [{"section": "Proof", "reason": "Proof: " + reason.format("proof")}]
        if proof:
            dropped.append({"section": "Proof", "reason": (
                f"The brief lists proof ({', '.join(proof)}) with stage pre-launch. If that proof is "
                f"real, set stage to live: {live['id']} shows it in its proof sections. The pre-launch "
                f"pattern shows none.")})
    else:
        entry, why = _best(entries, fields)

    seq = copy.deepcopy(entry)
    _without_phone(seq, contact)
    if seq["id"] != PRE_LAUNCH:
        dropped += _drop_unproven(seq, proof, contact)
    seq["why"] = why
    seq["dropped"] = dropped
    seq["proof_unknown"] = proof is None and any(s.get("proof") for s in seq["section_sequence"])
    return seq

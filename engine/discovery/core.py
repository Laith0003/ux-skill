"""10-field mandatory discovery protocol — the forcing function.

No generation is allowed until all ten fields are filled. This is the moat
against ``LLM-generates-generic-output`` because the LLM cannot improvise its
way past a structured prompt.

Public surface
--------------
``FIELDS``                       -- the canonical 10 fields
``DiscoveryState``               -- in-progress / complete state container
``next_question(state)``         -- returns the next unanswered field
``record(state, field, value)``  -- record an answer
``is_complete(state)``           -- True when all 10 fields are answered
``serialize(state)``             -- dict for ``.ux/last-discovery.json``
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


FIELDS: List[Dict[str, str]] = [
    {
        "id": "project_type",
        "label": "Project type",
        "hint": "landing | marketing-site | app-dashboard | admin-panel | docs | mobile-app | email",
    },
    {
        "id": "audience",
        "label": "Audience",
        "hint": "Who specifically — be concrete. 'B2B finance ops in MENA', not 'business users'.",
    },
    {
        "id": "primary_goal",
        "label": "Primary goal of this surface",
        "hint": "One job. 'Trial signup', 'Pricing comprehension', 'Dashboard at-a-glance status'.",
    },
    {
        "id": "tone",
        "label": "Tone (3-5 words)",
        "hint": "warm | editorial | precise | playful | clinical | confident | calm | bold | technical",
    },
    {
        "id": "must_have",
        "label": "Must-haves (hard constraints)",
        "hint": "dark-mode | RTL | AA accessibility | mobile-first | print-fidelity",
    },
    {
        "id": "forbidden",
        "label": "Forbidden (anti-list)",
        "hint": "Default-AI looks to avoid. Be specific. 'No purple-to-blue gradient. No three-card hero.'",
    },
    {
        "id": "reference_brands",
        "label": "Reference brands (3-5)",
        "hint": "Real brands whose design language fits. Pulled into the recommender as exemplars.",
    },
    {
        "id": "stack",
        "label": "Tech stack",
        "hint": "react | nextjs | vue | svelte | blade-alpine | astro | vanilla-html",
    },
    {
        "id": "region",
        "label": "Region / locale",
        "hint": "mena | us | eu | apac | global. Affects RTL, typography, color norms, copy style.",
    },
    {
        "id": "success_metric",
        "label": "Success metric",
        "hint": "How will you know it worked? 'Signup CR > 4%', 'TTI < 2s', 'Lighthouse > 95'.",
    },
]


@dataclass
class DiscoveryState:
    answers: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answers": dict(self.answers),
            "complete": is_complete(self),
            "missing": [f["id"] for f in FIELDS if f["id"] not in self.answers],
        }


def next_question(state: DiscoveryState) -> Optional[Dict[str, str]]:
    for f in FIELDS:
        if f["id"] not in state.answers:
            return f
    return None


def record(state: DiscoveryState, field_id: str, value: Any) -> DiscoveryState:
    if field_id not in {f["id"] for f in FIELDS}:
        raise KeyError(f"Unknown discovery field: {field_id}")
    state.answers[field_id] = value
    return state


def is_complete(state: DiscoveryState) -> bool:
    return all(f["id"] in state.answers for f in FIELDS)


def serialize(state: DiscoveryState) -> Dict[str, Any]:
    return state.to_dict()


def discover() -> DiscoveryState:
    """Compatibility shim — returns a blank state. Real interactive flow lives
    in ``engine/cli/discover.py``."""
    return DiscoveryState()

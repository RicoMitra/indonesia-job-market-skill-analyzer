"""Transparent title-based target-role rules."""

from __future__ import annotations

import re


ROLE_PATTERNS = {
    "Data Analyst": r"\bdata\s+analyst\b",
    "Data Scientist": r"\bdata\s+scientist\b",
    "ML Engineer": r"\b(?:machine\s+learning|ml)\s+engineer\b",
    "AI Engineer": r"\b(?:ai|artificial\s+intelligence)\s+engineer\b",
    "Business Analyst": r"\bbusiness\s+analyst\b",
    "Software Engineer": r"\b(?:software|backend|front[ -]?end|full[ -]?stack)\s+(?:engineer|developer)\b",
}


def map_roles(title: str) -> list[str]:
    normalized = title.lower()
    matches = [role for role, pattern in ROLE_PATTERNS.items() if re.search(pattern, normalized)]
    if re.search(r"\bdata\s*(?:&|and|/)\s*business\s+analyst\b", normalized):
        return ["Data Analyst", "Business Analyst"]
    return matches

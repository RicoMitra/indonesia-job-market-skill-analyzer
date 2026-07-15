"""Evidence-based skill-gap calculations."""

from __future__ import annotations

import pandas as pd

from src.extract_skills import SKILL_PATTERNS


def skill_gap(user_skills: list[str], role_skills: pd.DataFrame) -> dict[str, object]:
    canonical = {skill.lower(): skill for skill in SKILL_PATTERNS}
    entered = {canonical[value.strip().lower()] for value in user_skills if value.strip().lower() in canonical}
    ordered = role_skills.sort_values(["posting_count", "skill"], ascending=[False, True])["skill"].tolist()
    matched = [skill for skill in ordered if skill in entered]
    missing = [skill for skill in ordered if skill not in entered]
    coverage = round(100 * len(matched) / len(ordered), 1) if ordered else 0.0
    return {"matched": matched, "missing": missing, "coverage_percent": coverage}

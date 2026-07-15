"""Dictionary-backed skill extraction without external NLP services."""

from __future__ import annotations

import re


SKILL_PATTERNS = {
    "Python": [r"\bpython\b"],
    "SQL": [r"\bsql\b", r"\bpostgres(?:ql)?\b", r"\bmysql\b", r"\bsqlite\b"],
    "Excel": [r"\bexcel\b"],
    "Power BI": [r"\bpower\s*bi\b"],
    "Tableau": [r"\btableau\b"],
    "R": [r"\br\s+(?:programming|language)\b"],
    "Pandas": [r"\bpandas\b"],
    "scikit-learn": [r"\bscikit[- ]learn\b", r"\bsklearn\b"],
    "TensorFlow": [r"\btensorflow\b"],
    "PyTorch": [r"\bpytorch\b"],
    "Docker": [r"\bdocker\b"],
    "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b"],
    "GCP": [r"\bgcp\b", r"\bgoogle cloud\b"],
    "Azure": [r"\bazure\b"],
    "Git": [r"\bgit\b"],
    "Java": [r"\bjava\b"],
    "JavaScript": [r"\bjavascript\b"],
    "TypeScript": [r"\btypescript\b"],
    "React": [r"\breact(?:\.js)?\b"],
    "FastAPI": [r"\bfastapi\b"],
    "LLMs": [r"\bllms?\b", r"\blarge language models?\b"],
    "Communication": [r"\bcommunication\b"],
}


def extract_skills(text: str) -> list[str]:
    lowered = text.lower()
    return [skill for skill, patterns in SKILL_PATTERNS.items() if any(re.search(pattern, lowered) for pattern in patterns)]

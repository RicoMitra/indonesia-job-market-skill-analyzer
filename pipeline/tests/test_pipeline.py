import pandas as pd

from src.clean_data import clean_jobs
from src.extract_skills import extract_skills
from src.recommend import skill_gap
from src.roles import map_roles


def test_clean_jobs_deduplicates_and_preserves_canonical_columns():
    raw = pd.DataFrame(
        [
            {"title": "Data Analyst", "company": "Nusantara Data", "location": "Jakarta", "description": "Use SQL and Power BI."},
            {"title": "Data Analyst", "company": "Nusantara Data", "location": "Jakarta", "description": "Use SQL and Power BI."},
        ]
    )

    result = clean_jobs(raw, source="sample")

    assert len(result) == 1
    assert set(["job_id", "title", "company", "location", "description", "source"]).issubset(result.columns)


def test_role_mapping_allows_ambiguous_titles_to_match_multiple_roles():
    assert set(map_roles("Data & Business Analyst")) == {"Data Analyst", "Business Analyst"}
    assert map_roles("Office Administrator") == []


def test_skill_extraction_uses_aliases_and_word_boundaries():
    skills = extract_skills("Build Python services with PostgreSQL, Docker and Power BI; do not match sqlserver.")

    assert set(skills) == {"Python", "SQL", "Docker", "Power BI"}


def test_skill_gap_ranks_missing_observed_skills_and_ignores_unknown_input():
    role_skills = pd.DataFrame(
        [
            {"skill": "Python", "posting_count": 8},
            {"skill": "Docker", "posting_count": 6},
            {"skill": "SQL", "posting_count": 5},
        ]
    )

    result = skill_gap(["python", "unknown skill"], role_skills)

    assert result["matched"] == ["Python"]
    assert result["missing"] == ["Docker", "SQL"]
    assert result["coverage_percent"] == 33.3

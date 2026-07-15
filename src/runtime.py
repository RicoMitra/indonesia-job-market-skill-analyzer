"""Runtime setup required by the hosted Streamlit app."""

from pathlib import Path

from src.pipeline import run


def ensure_database(source: Path, database: Path) -> bool:
    """Build the bundled demo database once when a hosted filesystem starts empty."""
    if database.exists():
        return False
    run(source, database.parent, source="sample")
    return True

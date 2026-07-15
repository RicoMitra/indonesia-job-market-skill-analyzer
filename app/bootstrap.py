"""Make root-level project packages available to Streamlit entry points."""

import sys
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def add_project_root() -> Path:
    root = project_root()
    pipeline_root = root / "pipeline"
    if str(pipeline_root) not in sys.path:
        sys.path.insert(0, str(pipeline_root))
    return root

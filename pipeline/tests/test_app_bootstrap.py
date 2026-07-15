from app.bootstrap import project_root


def test_streamlit_entrypoint_identifies_repository_root():
    root = project_root()

    assert (root / "pipeline" / "src" / "database.py").exists()

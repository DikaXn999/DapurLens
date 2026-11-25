import os
import subprocess
import sys
import textwrap
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]


def run_python_without_dotenv(code, extra_env=None):
    env = os.environ.copy()
    env.pop("DATABASE_URL", None)
    env.pop("SECRET_KEY", None)

    if extra_env:
        env.update(extra_env)

    script = textwrap.dedent("""
        import sys
        import types

        dotenv = types.ModuleType("dotenv")
        dotenv.load_dotenv = lambda *args, **kwargs: None
        sys.modules["dotenv"] = dotenv

    """) + textwrap.dedent(code)

    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
    )


def test_missing_database_url_stops_application():
    result = run_python_without_dotenv("""
        import app.database
    """)

    assert result.returncode != 0
    assert "DATABASE_URL belum diatur" in result.stderr


def test_missing_secret_key_stops_application():
    result = run_python_without_dotenv(
        """
        import app.auth
        """,
        extra_env={"DATABASE_URL": "sqlite://"},
    )

    assert result.returncode != 0
    assert "SECRET_KEY belum diatur" in result.stderr

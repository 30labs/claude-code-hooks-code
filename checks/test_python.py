import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def session_path() -> str:
    """PATH without the environment pytest runs in."""
    venv = str(Path(sys.prefix) / "bin")
    parts = os.environ["PATH"].split(os.pathsep)
    return os.pathsep.join(p for p in parts if p != venv)


def test_hook_python_matches_pinned_version() -> None:
    pinned = (ROOT / ".python-version").read_text().strip()
    found = subprocess.run(
        ["python3", "-c", "import sys; print(sys.version)"],
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "PATH": session_path()},
    ).stdout
    assert found.startswith(pinned + "."), (
        f"python3 is {found.split()[0]}, hooks need {pinned}"
    )

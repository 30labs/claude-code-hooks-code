"""Run one formatter or linter on one file for after_edit.py."""

import shutil
import subprocess
from pathlib import Path

Command = list[str]


def call(command: Command, path: Path) -> str | None:
    """Run a tool on one file. Return its report on failure."""
    if shutil.which(command[0]) is None:
        return None
    result = subprocess.run(
        [*command, path.name],
        cwd=path.parent,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode == 0:
        return None
    return (result.stdout + result.stderr).strip()

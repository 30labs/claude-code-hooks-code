"""Helpers for stop_check.py: quiet git and a short report."""

import re
import subprocess
from pathlib import Path

MAX_FAILURES = 15
FAILURE_LINE = re.compile(r"^\S+:\d+: ")


def git(cwd: Path, *args: str) -> list[str]:
    """Return git's output lines, or [] if it exits non-zero."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        return []
    return result.stdout.splitlines()


def failure_report(stdout: str) -> list[str]:
    """Keep pytest's one-line failures and its summary line."""
    lines = stdout.strip().splitlines()
    failures = [x for x in lines if FAILURE_LINE.match(x)]
    summary = lines[-1] if lines else ""
    return [*failures[:MAX_FAILURES], summary]

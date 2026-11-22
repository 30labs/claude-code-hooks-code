"""Helpers for start.py: quiet git and short sections."""

import subprocess
from pathlib import Path

MAX_LINES = 15


def git(cwd: Path, *args: str) -> list[str]:
    """Return git's output lines, or [] if it exits non-zero."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        return []
    return result.stdout.splitlines()


def capped(lines: list[str]) -> list[str]:
    """Keep the first MAX_LINES lines and count the rest."""
    if len(lines) <= MAX_LINES:
        return lines
    more = len(lines) - MAX_LINES
    return [*lines[:MAX_LINES], f"(and {more} more)"]


def render(sections: dict[str, list[str]]) -> list[str]:
    """Format each non-empty section under its title."""
    return [
        f"{title}:\n" + "\n".join(f"  {x}" for x in capped(xs))
        for title, xs in sections.items()
        if xs
    ]

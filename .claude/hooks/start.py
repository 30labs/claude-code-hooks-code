"""Tell Claude where the project stands as a session starts."""

import json
from pathlib import Path

from hookkit import Event, field, run
from start_report import git, render


def failed_tests(cwd: Path) -> list[str]:
    cache = cwd / ".pytest_cache/v/cache/lastfailed"
    if not cache.is_file():
        return []
    data = json.loads(cache.read_text())
    return sorted(data) if isinstance(data, dict) else []


def main(event: Event) -> None:
    cwd = Path(field(event, "cwd") or ".")
    report = render({
        "Branch": git(cwd, "branch", "--show-current"),
        "Uncommitted": git(cwd, "status", "--short"),
        "Recent commits": git(cwd, "log", "--oneline", "-3"),
        "Failed on the last test run": failed_tests(cwd),
    })
    if report:
        print("Project state when this session started.")
        print("\n".join(report))


if __name__ == "__main__":
    run(main, fail_closed=False)

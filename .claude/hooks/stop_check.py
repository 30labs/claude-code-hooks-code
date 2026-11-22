"""Send Claude back to work when the tests fail."""

import re
import subprocess
import tempfile
from pathlib import Path

from hookkit import Event, field, respond, run
from stop_check_tools import failure_report, git

TESTS = [
    "uv", "run", "pytest",
    "-q", "--tb=line", "-p", "no:cacheprovider",
]
BASE = "main"
NO_TESTS_COLLECTED = 5
MAX_BLOCKS = 2
COUNTS = Path(tempfile.gettempdir()) / "stop-check"


def changed_python(cwd: Path) -> list[str]:
    status = git(cwd, "status", "--porcelain", "-uall")
    paths = []
    for line in status:
        path = line[3:]
        if "R" in line[:2] and " -> " in path:
            paths.extend(path.split(" -> ", 1))
        else:
            paths.append(path)
    base = git(cwd, "merge-base", "HEAD", BASE)
    if base:
        paths += git(cwd, "diff", "--name-only", base[0])
    return [p for p in paths if p.endswith(".py")]


def main(event: Event) -> None:
    cwd = Path(field(event, "cwd") or ".")
    if not changed_python(cwd):
        return
    result = subprocess.run(
        TESTS,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode in (0, NO_TESTS_COLLECTED):
        return

    counter = counter_for(event)
    blocks = blocks_so_far(event, counter)
    if blocks >= MAX_BLOCKS:
        return
    COUNTS.mkdir(exist_ok=True)
    counter.write_text(str(blocks + 1))
    respond({
        "decision": "block",
        "reason": "The test suite fails. Fix it, then finish.\n"
        + "\n".join(failure_report(result.stdout)),
    })


def counter_for(event: Event) -> Path:
    agent = field(event, "agent_id")
    owner = agent or field(event, "session_id")
    name = re.sub(r"\W", "", owner)
    return COUNTS / (name or "default")


def blocks_so_far(event: Event, counter: Path) -> int:
    if event.get("stop_hook_active") is not True:
        return 0
    if not counter.is_file():
        return 0
    return int(counter.read_text())


if __name__ == "__main__":
    run(main, fail_closed=False)

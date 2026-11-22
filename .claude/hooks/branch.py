"""Refuse git commit while the current branch is main."""

import re
import subprocess

from hookkit import Event, block, field, run

PROTECTED = {"main", "master"}
COMMIT = re.compile(r"(?:^|[;&|\n])\s*git\s+commit\b")


def current_branch(cwd: str) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=cwd or None,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout.strip()


def main(event: Event) -> None:
    command = field(event, "tool_input", "command")
    if not COMMIT.search(command):
        return
    branch = current_branch(field(event, "cwd"))
    if branch in PROTECTED:
        block(
            f"Commits to {branch} are not allowed here.\n"
            "Run git switch -c <name> as its own command,\n"
            "then commit in a separate command."
        )


if __name__ == "__main__":
    run(main, fail_closed=True)

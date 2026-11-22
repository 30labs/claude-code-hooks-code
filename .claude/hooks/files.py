"""Keep Claude out of secrets and generated files."""

import os
from fnmatch import fnmatch
from pathlib import Path

from files_rules import (
    SAFE_NAMES,
    SECRET_DIRS,
    SECRET_NAMES,
    WORD_BREAK,
    WRITE_TOOLS,
    write_problem,
)
from hookkit import Event, field, respond, run


def is_secret(path: Path) -> bool:
    if SECRET_DIRS & set(path.parts):
        return True
    if path.name in SAFE_NAMES:
        return False
    return any(fnmatch(path.name, p) for p in SECRET_NAMES)


def project_root(event: Event) -> Path:
    root = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(root or field(event, "cwd")).resolve()


def file_problem(
    tool: str, raw: str, root: Path
) -> str | None:
    path = Path(raw).resolve()
    if is_secret(path):
        return (
            f"{path.name} holds secrets and is off limits.\n"
            "Ask the user for the value you need."
        )
    if tool not in WRITE_TOOLS:
        return None
    if not path.is_relative_to(root):
        return (
            f"{path} is outside the project.\n"
            "Only change files inside the project."
        )
    return write_problem(path.relative_to(root))


def bash_problem(command: str) -> str | None:
    for word in WORD_BREAK.split(command):
        if word and is_secret(Path(word)):
            return (
                f"The command touches {word}.\n"
                "It holds secrets. Ask the user instead."
            )
    return None


def main(event: Event) -> None:
    tool = field(event, "tool_name")
    if tool == "Bash":
        command = field(event, "tool_input", "command")
        reason = bash_problem(command)
    else:
        raw = field(event, "tool_input", "file_path")
        root = project_root(event)
        reason = file_problem(tool, raw, root) if raw else None
    if reason:
        respond({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        })


if __name__ == "__main__":
    run(main, fail_closed=True)

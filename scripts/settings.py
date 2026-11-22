"""Write .claude/settings.json from a table of hooks."""

import json
from pathlib import Path

from settings_build import Group, build

GROUPS: list[Group] = [
    ("SessionStart", "startup|resume|compact", ["start.py"]),
    ("SessionStart", None, ["audit.py"]),
    ("UserPromptSubmit", None, ["prompt_guard.py", "audit.py"]),
    ("PreToolUse", "Bash", ["branch.py", "guard.py"]),
    ("PreToolUse", "Read|Write|Edit|Bash", ["files.py"]),
    ("PreToolUse", None, ["audit.py"]),
    ("PostToolUse", "Write|Edit", ["after_edit.py"]),
    ("PostToolUse", None, ["audit.py"]),
    ("PostToolUseFailure", None, ["audit.py"]),
    ("Stop", None, ["stop_check.py", "audit.py"]),
    ("SubagentStop", None, ["stop_check.py"]),
]


GUARD_SCRIPTS = {"branch.py", "guard.py", "files.py"}


def command(script: str) -> dict[str, str]:
    path = f"$CLAUDE_PROJECT_DIR/.claude/hooks/{script}"
    hook = {"type": "command", "command": f'python3 "{path}"'}
    if script in GUARD_SCRIPTS:
        hook["onFailure"] = "block"
    return hook


if __name__ == "__main__":
    target = Path(".claude/settings.json")
    target.parent.mkdir(exist_ok=True)
    settings = build(GROUPS, command)
    target.write_text(json.dumps(settings, indent=2) + "\n")

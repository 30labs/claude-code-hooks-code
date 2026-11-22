"""Read the hook commands a settings file registers."""

import json
import re
from pathlib import Path

SCRIPT = re.compile(r"\$CLAUDE_PROJECT_DIR/(\S+?\.py)")


def registered_commands(settings: Path) -> list[str]:
    """Every command handler's command, across all events."""
    hooks = json.loads(settings.read_text()).get("hooks", {})
    return [
        handler["command"]
        for groups in hooks.values()
        for group in groups
        for handler in group["hooks"]
        if handler.get("type") == "command"
    ]


def script_of(command: str, root: Path) -> Path | None:
    """The script named through $CLAUDE_PROJECT_DIR, if any."""
    match = SCRIPT.search(command)
    return root / match.group(1) if match else None

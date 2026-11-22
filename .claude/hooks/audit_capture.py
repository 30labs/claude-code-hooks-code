"""Save whole events as fixtures: audit.py's capture mode."""

import json
from datetime import datetime
from pathlib import Path

from hookkit import Event, field


def capture(
    event: Event, directory: Path, now: datetime
) -> None:
    """Write the event as <event>-<tool or source>-<tag>.json"""
    tag = field(event, "tool_use_id")[-8:]
    name = "-".join(
        part
        for part in (
            field(event, "hook_event_name"),
            field(event, "tool_name") or field(event, "source"),
            tag or f"{now:%Y%m%dT%H%M%S%f}",
        )
        if part
    )
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}.json"
    path.write_text(json.dumps(event, indent=2) + "\n")

"""Append one line per hook event to a daily audit log."""

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from audit_capture import capture
from audit_text import redact, summary
from hookkit import Event, field, run


def record(event: Event, now: datetime) -> dict[str, object]:
    fields: dict[str, object] = {
        "time": now.isoformat(timespec="seconds"),
        "session": field(event, "session_id")[:8],
        "event": field(event, "hook_event_name"),
        "tool": field(event, "tool_name"),
        "id": field(event, "tool_use_id"),
        "what": summary(event),
        "error": redact(field(event, "error")),
    }
    if isinstance(event.get("duration_ms"), int):
        fields["ms"] = event["duration_ms"]
    return {k: v for k, v in fields.items() if v != ""}


def main(event: Event) -> None:
    root = os.environ.get("CLAUDE_PROJECT_DIR")
    base = Path(root or field(event, "cwd") or ".")
    now = datetime.now(UTC)
    log = base / ".claude" / "audit" / f"{now:%Y-%m-%d}.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as out:
        out.write(json.dumps(record(event, now)) + "\n")
    target = os.environ.get("HOOK_CAPTURE")
    if target:
        capture(event, Path(target), now)


if __name__ == "__main__":
    run(main, fail_closed=False)

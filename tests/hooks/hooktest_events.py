"""Events shaped like the ones Claude Code sends, for tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def bash_event(command: str) -> dict[str, object]:
    """A PreToolUse event for the Bash tool running command."""
    return {
        "session_id": "test",
        "transcript_path": "/tmp/transcript.jsonl",
        "cwd": str(ROOT),
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "tool_use_id": "toolu_test",
    }

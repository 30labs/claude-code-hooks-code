"""Loading and the simpler sections of report.py."""

import json
from collections import Counter
from pathlib import Path

Record = dict[str, object]


def load(paths: list[str]) -> list[Record]:
    """Every record in the given JSONL files, in order."""
    return [
        json.loads(line)
        for path in paths
        for line in Path(path).read_text().splitlines()
        if line.strip()
    ]


def tool_counts(records: list[Record]) -> dict[str, int]:
    """Tool calls per tool, most used first."""
    calls = {
        str(r["id"]): r
        for r in records
        if r["event"] == "PreToolUse" and "id" in r
    }
    tools = Counter(str(r.get("tool")) for r in calls.values())
    return dict(tools.most_common())


def failed(records: list[Record]) -> list[str]:
    """One line per failed tool call."""
    return [
        f"Failed: {r.get('what')}"
        for r in records
        if r["event"] == "PostToolUseFailure"
    ]


def slowest(records: list[Record], count: int) -> list[str]:
    """The slowest timed records, slowest first."""
    timed = [r for r in records if isinstance(r.get("ms"), int)]
    timed.sort(key=lambda r: int(str(r["ms"])), reverse=True)
    return [
        f"Slow: {r.get('what')} ({r['ms']} ms)"
        for r in timed[:count]
    ]

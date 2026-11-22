"""Total token usage in a Claude Code transcript, per model."""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from usage_table import KINDS, show


def totals(path: Path) -> dict[str, Counter[str]]:
    seen: set[str] = set()
    result: dict[str, Counter[str]] = defaultdict(Counter)
    for line in path.read_text().splitlines():
        record = json.loads(line)
        message = record.get("message")
        if not isinstance(message, dict):
            continue
        msg_id = str(message.get("id"))
        if record.get("type") != "assistant" or msg_id in seen:
            continue
        seen.add(msg_id)
        usage = message.get("usage") or {}
        counts = result[str(message.get("model"))]
        for kind in KINDS:
            counts[kind] += int(usage.get(kind, 0))
    return dict(result)


if __name__ == "__main__":
    show(totals(Path(sys.argv[1])))

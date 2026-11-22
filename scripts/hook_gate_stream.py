"""Read a claude -p stream-json run for hook_gate.py.

Blank lines are skipped. Every hook_response record is sorted by
its outcome: a cancelled hook goes into ``cancelled`` and is not
judged on its exit code, since a hook killed at teardown has
none; every other response is kept in ``responses`` and its name
added to ``ran``. The last record of type ``result`` is the
run's outcome, and ``result`` stays None when the stream ends
without one.
"""

import json
from dataclasses import dataclass, field
from typing import Any

Record = dict[str, Any]


@dataclass
class Stream:
    responses: list[Record] = field(default_factory=list)
    ran: set[str] = field(default_factory=set)
    cancelled: set[str] = field(default_factory=set)
    result: Record | None = None


def read_stream(lines: list[str]) -> Stream:
    stream = Stream()
    for line in lines:
        if not line.strip():
            continue
        record: Record = json.loads(line)
        if record.get("subtype") == "hook_response":
            name = record["hook_name"]
            if record.get("outcome") == "cancelled":
                stream.cancelled.add(name)
                continue
            stream.ran.add(name)
            stream.responses.append(record)
        elif record.get("type") == "result":
            stream.result = record
    return stream

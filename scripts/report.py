"""Summarise audit logs given on the command line."""

import sys

from report_sections import failed, load, slowest, tool_counts

DONE = {"PostToolUse", "PostToolUseFailure"}
Record = dict[str, object]


def unfinished(records: list[Record]) -> list[Record]:
    calls = {
        str(r["id"]): r
        for r in records
        if r["event"] == "PreToolUse" and "id" in r
    }
    done = {str(r["id"]) for r in records if r["event"] in DONE}
    return [c for i, c in calls.items() if i not in done]


def main(paths: list[str]) -> None:
    records = load(paths)
    print("Tool calls:", tool_counts(records))
    for call in unfinished(records):
        print("No outcome:", call.get("what"))
    for line in [*failed(records), *slowest(records, 3)]:
        print(line)


if __name__ == "__main__":
    main(sys.argv[1:])

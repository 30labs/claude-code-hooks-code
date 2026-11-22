"""Fail a CI step when hooks did not run or blocked work.

Usage: python3 hook_gate.py HOOK_NAME ... < run.jsonl
"""

import sys

from hook_gate_stream import Stream, read_stream

HOOK_ANSWER = {0, 2}


def broken_hooks(stream: Stream) -> list[str]:
    problems: list[str] = []
    for record in stream.responses:
        code = record.get("exit_code")
        if code in HOOK_ANSWER:
            continue
        name = record["hook_name"]
        if code is None:
            problems.append(f"{name} has no exit_code")
        else:
            problems.append(f"{name} exited {code}")
        stderr = record.get("stderr") or ""
        for text in stderr.splitlines():
            problems.append(f"  {text}")
    return problems


def missing_hooks(stream: Stream, need: list[str]) -> list[str]:
    problems: list[str] = []
    for name in need:
        if name in stream.ran:
            continue
        if name in stream.cancelled:
            problems.append(f"{name} was cancelled")
        else:
            problems.append(f"{name} never ran")
    return problems


def run_problems(stream: Stream) -> list[str]:
    result = stream.result
    if result is None:
        return ["no result record: run did not end"]
    problems: list[str] = []
    if result["is_error"]:
        problems.append(f"run failed: {result['subtype']}")
    for denial in result["permission_denials"]:
        given = denial["tool_input"]
        what = given.get("command") or given.get("file_path")
        problems.append(f"denied {denial['tool_name']}: {what}")
    return problems


def main() -> int:
    stream = read_stream(sys.stdin.read().splitlines())
    problems = broken_hooks(stream)
    problems += missing_hooks(stream, sys.argv[1:])
    problems += run_problems(stream)
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

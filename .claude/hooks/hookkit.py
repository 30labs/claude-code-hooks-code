"""Shared helpers for Claude Code command hooks."""

import json
import sys
from collections.abc import Callable
from typing import Any, NoReturn

Event = dict[str, Any]


def read_event() -> Event:
    data = json.load(sys.stdin)
    if not isinstance(data, dict):
        raise ValueError("input is not a JSON object")
    return data


def field(obj: Event, *path: str) -> str:
    """Return a nested string field, or "" if absent."""
    value: Any = obj
    for key in path:
        if not isinstance(value, dict):
            return ""
        value = value.get(key)
    return value if isinstance(value, str) else ""


def block(reason: str) -> NoReturn:
    print(reason, file=sys.stderr)
    sys.exit(2)


def respond(output: Event) -> NoReturn:
    print(json.dumps(output))
    sys.exit(0)


def run(
    main: Callable[[Event], None], *, fail_closed: bool
) -> NoReturn:
    try:
        main(read_event())
    except SystemExit:
        raise
    except Exception as exc:
        problem = f"hook error: {type(exc).__name__}: {exc}"
        if fail_closed:
            block(problem + "\nblocked to be safe")
        print(problem, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

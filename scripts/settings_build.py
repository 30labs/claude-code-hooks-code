"""Turn settings.py's table of hooks into settings.json.

Each row becomes one group under its event, in table order, so
two rows for the same event become two entries in that event's
list. A row with no matcher gets no ``matcher`` key, which for
tool events means every tool. ``command`` turns one script name
into its handler.
"""

from collections.abc import Callable

Group = tuple[str, str | None, list[str]]
Handler = dict[str, str]


def build(
    groups: list[Group], command: Callable[[str], Handler]
) -> dict[str, object]:
    hooks: dict[str, list[dict[str, object]]] = {}
    for event, matcher, scripts in groups:
        group: dict[str, object] = {
            "hooks": [command(s) for s in scripts]
        }
        if matcher:
            group["matcher"] = matcher
        hooks.setdefault(event, []).append(group)
    return {"hooks": hooks}

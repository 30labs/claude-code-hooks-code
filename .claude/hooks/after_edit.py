"""Fix, format and lint each file after Claude writes it."""

from pathlib import Path

from after_edit_tools import Command, call
from hookkit import Event, block, field, respond, run

RUFF_CHECK = [
    "ruff", "check", "--quiet", "--output-format", "concise",
]
FIXERS: dict[str, list[Command]] = {
    ".py": [[*RUFF_CHECK, "--fix", "--exit-zero"]],
}
FORMATTERS: dict[str, list[Command]] = {
    ".py": [["ruff", "format", "--quiet"]],
}
LINTERS: dict[str, list[Command]] = {
    ".py": [RUFF_CHECK],
}


def main(event: Event) -> None:
    raw = field(event, "tool_input", "file_path")
    path = Path(raw)
    if not raw or not path.is_file():
        return
    before = path.read_bytes()
    for command in FIXERS.get(path.suffix, []):
        call(command, path)
    for command in FORMATTERS.get(path.suffix, []):
        call(command, path)
    reports = [
        report
        for command in LINTERS.get(path.suffix, [])
        if (report := call(command, path))
    ]

    changed = path.read_bytes() != before
    note = (
        f"{path.name} was changed by a hook.\n"
        "Read it again before you edit it."
    )
    if reports:
        block(
            "\n".join(reports)
            + "\nFix these before moving on."
            + (f"\n{note}" if changed else "")
        )
    if changed:
        respond({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": note,
            }
        })


if __name__ == "__main__":
    run(main, fail_closed=False)

"""Block destructive shell commands before they run."""

import re
from collections.abc import Callable

from guard_rm import rm_rule
from guard_shell import Words, flags, split_commands
from hookkit import Event, block, field, run

Rule = Callable[[Words], str | None]


def git_rule(words: Words) -> str | None:
    if words[0] != "git" or len(words) < 2:
        return None
    sub, f = words[1], flags(words)
    if sub == "push" and f & {"-f", "--force"}:
        return (
            "git push --force rewrites shared history.\n"
            "Use --force-with-lease, or ask the user."
        )
    if sub == "reset" and "--hard" in f:
        return (
            "git reset --hard discards uncommitted work.\n"
            "Use git stash, or ask the user."
        )
    if sub == "clean" and f & {"-f", "--force"}:
        return (
            "git clean -f deletes untracked files.\n"
            "List them with git clean -n and ask the user."
        )
    return None


PIPE_TO_SHELL = re.compile(
    r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z)?sh\b"
)
ROUGH_RM = re.compile(r"\brm\s+-\w*\s+[/~$]")

RULES: list[Rule] = [rm_rule, git_rule]


def verdict(line: str) -> str | None:
    if PIPE_TO_SHELL.search(line):
        return (
            "Piping a download into a shell runs unseen code.\n"
            "Download the script, show it, and ask the user."
        )
    try:
        commands = split_commands(line)
    except ValueError:
        if ROUGH_RM.search(line):
            return "Unparseable command with rm on a root path."
        return None
    for words in commands:
        for rule in RULES:
            reason = rule(words)
            if reason:
                return reason
    return None


def main(event: Event) -> None:
    reason = verdict(field(event, "tool_input", "command"))
    if reason:
        block(reason)


if __name__ == "__main__":
    run(main, fail_closed=True)

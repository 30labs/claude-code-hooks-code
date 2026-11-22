"""Shell parsing for guard.py: a line into its commands."""

import re
import shlex

Words = list[str]

SEPARATORS = {";", "&&", "||", "|", "&", "(", ")"}
WRAPPERS = {"sudo", "env", "command", "exec", "nohup", "time"}
SHELLS = {"sh", "bash", "zsh"}
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
REDIRECT = re.compile(r"[<>&|]*[<>][<>&|]*")
ROUGH_RM = re.compile(
    r"\brm\b"
    r"(?=[^;&|]*(?:--recursive|-\w*[rR]\w*))"
    r"(?=[^;&|]*(?:--force|-\w*f\w*))"
    r"[^;&|]*\s[/~$]"
)


def split_commands(line: str) -> list[Words]:
    """Return each command on the line as words, unwrapped.

    Raises ValueError when the line's quotes do not balance.
    """
    lexer = shlex.shlex(
        line.replace("\n", " ; "),
        posix=True,
        punctuation_chars=True,
    )
    lexer.whitespace_split = True
    commands: list[Words] = [[]]
    target = False
    for token in lexer:
        words = commands[-1]
        if target:
            target = False
        elif token in SEPARATORS:
            commands.append([])
        elif REDIRECT.fullmatch(token):
            if words and words[-1].isdigit():
                words.pop()
            target = True
        else:
            words.append(token)
    found: list[Words] = []
    for words in commands:
        words = unwrap(words)
        if not words:
            continue
        if words[0] in SHELLS and "-c" in words[1:-1]:
            script = words[words.index("-c") + 1]
            found.extend(split_commands(script))
        else:
            found.append(words)
    return found


def unwrap(words: Words) -> Words:
    """Drop wrappers, assignments and the program's path."""
    while words and (
        words[0] in WRAPPERS or ASSIGNMENT.match(words[0])
    ):
        if words[0] == "sudo":
            words = sudo_command(words)
        else:
            words = words[1:]
    if words:
        words = [words[0].rsplit("/", 1)[-1], *words[1:]]
    return words


def sudo_command(words: Words) -> Words:
    """Skip supported sudo options before its command."""
    words = words[1:]
    while words:
        if words[0] == "--":
            return words[1:]
        if words[0] in {"-u", "-g"}:
            words = words[2:]
        elif words[0].startswith("--user="):
            words = words[1:]
        elif words[0] in {"-E", "-H", "-n", "-i", "-s"}:
            words = words[1:]
        else:
            return words
    return words


def flags(words: Words) -> set[str]:
    """Return a command's flags; -rf counts as -r and -f."""
    found: set[str] = set()
    for word in words[1:]:
        if word.startswith("--"):
            found.add(word)
        elif word.startswith("-"):
            found.update(f"-{c}" for c in word[1:])
    return found

"""The rule tables behind files.py, and its write-only rules."""

import re
from fnmatch import fnmatch
from pathlib import Path

SECRET_NAMES = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "id_rsa*",
    "id_dsa*",
    "id_ecdsa*",
    "id_ed25519*",
)
SAFE_NAMES = {".env.example", ".env.sample"}
SECRET_DIRS = {".ssh", ".aws", ".gnupg"}
LOCKFILES = {"uv.lock", "package-lock.json", "poetry.lock"}
READ_ONLY_DIRS = {"generated"}
GIT_DIR = ".git"
HOOK_FILES = (".claude/hooks/*", ".claude/settings*.json")
WRITE_TOOLS = {"Write", "Edit"}
WORD_BREAK = re.compile(r"[\s;&|<>()'\"=]+")


def write_problem(rel: Path) -> str | None:
    """Refuse changes to project files Claude may only read."""
    if rel.name in LOCKFILES:
        return (
            f"{rel} is written by the package manager.\n"
            "Change dependencies with its CLI instead."
        )
    if GIT_DIR in rel.parts:
        return (
            f"{rel} is git's own data, not a project file.\n"
            "Ask the user before changing it."
        )
    if any(fnmatch(str(rel), p) for p in HOOK_FILES):
        return (
            f"{rel} runs or configures hooks.\n"
            "Hooks change through review. Tell the user\n"
            "what you would change and why."
        )
    if READ_ONLY_DIRS & set(rel.parts):
        return (
            f"{rel} is generated, not edited by hand.\n"
            "Change the source it is generated from."
        )
    return None

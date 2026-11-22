"""The rm rule for guard.py: deletes that reach too far."""

from guard_shell import Words, flags


def segments(path: str) -> list[str]:
    return [p for p in path.split("/") if p not in {"", "."}]


def inside_project(path: str) -> bool:
    return not (
        path.startswith(("/", "~", "$"))
        or ".." in segments(path)
    )


def rm_rule(words: Words) -> str | None:
    if words[0] != "rm":
        return None
    f = flags(words)
    recursive = f & {"-r", "-R", "--recursive"}
    force = f & {"-f", "--force"}
    targets = [w for w in words[1:] if not w.startswith("-")]
    if not (recursive and force):
        return None
    outside = [t for t in targets if not inside_project(t)]
    if outside or not targets:
        where = " ".join(outside) or "(no target)"
        return (
            f"rm -rf outside the project: {where}\n"
            "Delete named paths inside the project."
        )
    whole = [t for t in targets if segments(t) in ([], ["*"])]
    if whole:
        return (
            f"rm -rf aims at the whole directory: {whole[0]}\n"
            "Delete named paths inside it instead."
        )
    return None

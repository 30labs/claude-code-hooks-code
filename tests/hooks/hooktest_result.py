"""What a hook run returns: its exit code and both streams."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    code: int
    stdout: str
    stderr: str

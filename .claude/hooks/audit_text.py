"""Turn an event into the one redacted line audit.py records."""

import re

from hookkit import Event, field

SECRET = re.compile(
    r"AKIA[0-9A-Z]{16}"
    r"|gh[pousr]_[A-Za-z0-9]{36}"
    r"|ghs_[0-9]+_[\w.-]{20,}"
    r"|github_pat_\w{20,}"
    r"|(?i:password|token|secret)=\S+"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----.*"
)
MAX_TEXT = 200
TOOL_KEYS = ("command", "file_path", "url", "pattern")
EVENT_KEYS = ("prompt", "source", "reason")


def redact(text: str) -> str:
    """One line, credentials replaced, then cut to MAX_TEXT."""
    one_line = " ".join(text.split())
    return SECRET.sub("[redacted]", one_line)[:MAX_TEXT]


def summary(event: Event) -> str:
    """The first field that says what the event was about."""
    for key in TOOL_KEYS:
        value = field(event, "tool_input", key)
        if value:
            return redact(value)
    for key in EVENT_KEYS:
        value = field(event, key)
        if value:
            return redact(value)
    return ""

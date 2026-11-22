"""Stop prompts that contain credentials."""

import re

from hookkit import Event, block, field, run

PATTERNS = {
    "an AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "a GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{36}\b",
    "a GitHub App token": r"\bghs_[0-9]+_[\w.-]{20,}",
    "a fine-grained GitHub token": r"\bgithub_pat_\w{20,}",
    "a private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}


def main(event: Event) -> None:
    prompt = field(event, "prompt")
    for label, pattern in PATTERNS.items():
        if re.search(pattern, prompt):
            block(
                f"This prompt contains {label}.\n"
                "Remove it and send the prompt again."
            )


if __name__ == "__main__":
    run(main, fail_closed=False)

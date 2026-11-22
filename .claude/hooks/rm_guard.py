"""The test guard from this chapter's runs, minus logging."""

import json
import sys

event = json.load(sys.stdin)
command = event.get("tool_input", {}).get("command", "")
if "rm " in command:
    message = "guard: rm is not allowed in this project"
    print(message, file=sys.stderr)
    sys.exit(2)

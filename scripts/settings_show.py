"""Print .claude/settings.json one group per line.

Each line is the event, the matcher (``*`` when there is none)
and the script names in order. A ``!`` follows a script whose
handler sets ``"onFailure": "block"``.
"""

import json
from pathlib import Path


def main() -> None:
    path = Path(".claude/settings.json")
    settings = json.loads(path.read_text())
    for event, groups in settings["hooks"].items():
        for group in groups:
            scripts = []
            for hook in group["hooks"]:
                script = hook["command"].split("/")[-1]
                name = script.rstrip('"')
                if hook.get("onFailure") == "block":
                    name += "!"
                scripts.append(name)
            where = group.get("matcher", "*")
            print(f"{event} [{where}]:", " ".join(scripts))


if __name__ == "__main__":
    main()

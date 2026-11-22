import subprocess

import pytest

from hooktest import ROOT
from hooktest_settings import registered_commands, script_of

COMMANDS = registered_commands(ROOT / ".claude/settings.json")


@pytest.mark.parametrize("command", COMMANDS)
def test_hook_script_exists_and_imports(command: str) -> None:
    script = script_of(command, ROOT)
    assert script, f"no $CLAUDE_PROJECT_DIR script: {command}"
    assert script.is_file(), f"missing hook script: {script}"
    proc = subprocess.run(
        [command.split()[0], "-c", f"import {script.stem}"],
        cwd=script.parent,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr

"""Run Claude Code hooks the way Claude Code does."""

import json
import os
import subprocess
import sys
from pathlib import Path

from hooktest_result import Result

ROOT = Path(__file__).resolve().parents[2]
HOOKS = ROOT / ".claude" / "hooks"


def run_hook(name: str, event: object) -> Result:
    raw = event if isinstance(event, str) else json.dumps(event)
    proc = subprocess.run(
        [sys.executable, str(HOOKS / f"{name}.py")],
        input=raw,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)},
    )
    return Result(proc.returncode, proc.stdout, proc.stderr)

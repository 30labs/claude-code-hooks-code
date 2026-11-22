import json
from pathlib import Path

import pytest

from hooktest import run_hook

EVENTS = Path(__file__).parent / "events"
CASES = sorted(EVENTS.glob("*/*.json"))


@pytest.mark.parametrize(
    "path", CASES, ids=lambda p: f"{p.parent.name}/{p.stem}"
)
def test_recorded_event(path: Path) -> None:
    expected = {"block": 2, "allow": 0}[path.stem.split("-")[0]]
    event = json.loads(path.read_text())
    assert run_hook(path.parent.name, event).code == expected

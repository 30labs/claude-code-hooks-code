import pytest

from guard import verdict
from hooktest import run_hook
from hooktest_cases import MORE_ALLOWED, MORE_BLOCKED
from hooktest_events import bash_event
from hooktest_result import Result

BLOCKED = [
    "git reset --hard HEAD~3",
    "cat <<EOF\ndon't\nEOF\nrm -rf ~/",
    *MORE_BLOCKED,
]
ALLOWED = [
    "echo 'rm -rf /' >> notes.md",
    *MORE_ALLOWED,
]


@pytest.mark.parametrize("command", BLOCKED)
def test_blocks(command: str) -> None:
    assert verdict(command) is not None


@pytest.mark.parametrize("command", ALLOWED)
def test_allows(command: str) -> None:
    assert verdict(command) is None


def test_block_is_exit_2_with_reason_on_stderr() -> None:
    result = run_hook("guard", bash_event("git reset --hard"))
    assert (result.code, result.stdout) == (2, "")
    assert "git stash" in result.stderr


def test_allow_is_exit_0_and_silent() -> None:
    result = run_hook("guard", bash_event("ls -la"))
    assert result == Result(0, "", "")


def test_bad_input_fails_closed() -> None:
    result = run_hook("guard", "not json")
    assert result.code == 2
    assert "hook error" in result.stderr

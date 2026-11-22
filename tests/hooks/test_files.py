import pytest

from files import file_problem
from hooktest import ROOT
from hooktest_cases import HOOK_FILES


@pytest.mark.parametrize("rel", HOOK_FILES)
def test_hook_files_refuse_edits(rel: str) -> None:
    path = str(ROOT / rel)
    assert file_problem("Edit", path, ROOT) is not None
    assert file_problem("Read", path, ROOT) is None

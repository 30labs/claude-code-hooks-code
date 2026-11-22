import pytest

from files import file_problem
from hooktest import ROOT
from hooktest_cases import HOOK_FILES, SECRET_FILES


@pytest.mark.parametrize("rel", HOOK_FILES + SECRET_FILES)
def test_file_rules(rel: str) -> None:
    path = str(ROOT / rel)
    assert file_problem("Edit", path, ROOT) is not None
    read = file_problem("Read", path, ROOT)
    assert (read is not None) == (rel in SECRET_FILES)

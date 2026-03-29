import os
from pathlib import Path

import pytest

from .pytest_plugin import filepath as filepath


@pytest.mark.parametrize("filename", ["filename.py", "thispathdoesnotexist.txt", "nested/folder"])
def test_filename_to_filepath(filename: str, filepath: Path) -> None:
    assert filename == os.fspath(filepath)
    assert isinstance(filepath, Path)

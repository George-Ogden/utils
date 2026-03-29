import builtins
import os
from pathlib import Path

from debug import CONFIG
import pytest

from .pytest_plugin import filepath as filepath
from .pytest_plugin import setup_debug as setup_debug


@pytest.mark.parametrize("filename", ["filename.py", "thispathdoesnotexist.txt", "nested/folder"])
def test_filename_to_filepath(filename: str, filepath: Path) -> None:
    assert filename == os.fspath(filepath)
    assert isinstance(filepath, Path)


def test_debug() -> None:
    assert "dbg" in builtins.__dict__
    assert CONFIG.sort_unordered_collections

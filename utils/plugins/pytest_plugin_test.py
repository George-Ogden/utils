import builtins
import os
from pathlib import Path
import random

from debug import CONFIG
import pytest

from .pytest_plugin import filepath as filepath
from .pytest_plugin import manual_seed as manual_seed
from .pytest_plugin import seed as seed
from .pytest_plugin import setup_debug as setup_debug
from .pytest_plugin import test_dir as test_dir
from .pytest_plugin import test_path as test_path


@pytest.mark.parametrize("filename", ["filename.py", "thispathdoesnotexist.txt", "nested/folder"])
def test_filename_to_filepath(filename: str, filepath: Path) -> None:
    assert filename == os.fspath(filepath)
    assert isinstance(filepath, Path)


def test_debug() -> None:
    assert "dbg" in builtins.__dict__
    assert CONFIG.sort_unordered_collections


def test_automatic_seed() -> None:
    pre_seeded = [random.random() for _ in range(10)]
    random.seed(0)
    seeded = [random.random() for _ in range(10)]
    assert pre_seeded == seeded


@pytest.mark.parametrize("seed", range(5))
def test_manual_seed(seed: int) -> None:
    pre_seeded = [random.random() for _ in range(10)]
    random.seed(seed)
    seeded = [random.random() for _ in range(10)]
    assert pre_seeded == seeded


@pytest.mark.parametrize("seed", range(5))
def test_manual_seed_value(seed: int, manual_seed: int) -> None:
    assert manual_seed == seed
    pre_seeded = [random.random() for _ in range(10)]
    random.seed(seed)
    seeded = [random.random() for _ in range(10)]
    assert pre_seeded == seeded


@pytest.mark.typed
def test_test_path(test_path: Path) -> None:
    assert test_path == Path("utils/plugins/pytest_plugin_test.py").absolute()


@pytest.mark.typed
def test_test_dir(test_dir: Path) -> None:
    assert test_dir == Path("utils/plugins").absolute()

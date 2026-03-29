from pathlib import Path

import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_debug() -> None:
    try:
        from debug import CONFIG, install
    except ImportError:
        ...
    else:
        install()
        CONFIG.sort_unordered_collections = True


@pytest.fixture
def filepath(filename: str) -> Path:
    return Path(filename)

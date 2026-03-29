from pathlib import Path

import pytest


@pytest.fixture
def filepath(filename: str) -> Path:
    return Path(filename)

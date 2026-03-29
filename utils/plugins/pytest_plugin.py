from pathlib import Path
import random

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


@pytest.fixture
def seed() -> int:
    return 0


@pytest.fixture(autouse=True)
def manual_seed(seed: int) -> int:
    random.seed(seed)
    try:
        import numpy as np
    except ImportError:
        ...
    else:
        np.random.seed(seed)
    try:
        import torch as th  # type:ignore[import-not-found]
    except ImportError:
        ...
    else:
        th.random.manual_seed(seed)
    return seed

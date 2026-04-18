import pytest

from . import unimplemented


def test_unimplemented_no_args() -> None:
    with pytest.raises(NotImplementedError):
        unimplemented()

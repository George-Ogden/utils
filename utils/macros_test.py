import pytest

from . import unimplemented


def test_unimplemented_no_args() -> None:
    with pytest.raises(NotImplementedError):
        unimplemented()


def test_unimplemented_arg() -> None:
    with pytest.raises(NotImplementedError) as e:
        unimplemented("doesn't make sense to implement")
    assert "doesn't make sense to implement" in str(e)

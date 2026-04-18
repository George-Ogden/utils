import pytest

from . import NotImplementedYetError, todo, unimplemented


def test_unimplemented_no_args() -> None:
    with pytest.raises(NotImplementedError):
        unimplemented()


def test_unimplemented_arg() -> None:
    with pytest.raises(NotImplementedError) as e:
        unimplemented("doesn't make sense to implement")
    assert "doesn't make sense to implement" in str(e)


def test_todo_no_args() -> None:
    with pytest.raises(NotImplementedError):
        todo()
    with pytest.raises(NotImplementedYetError):
        todo()


def test_todo_arg() -> None:
    with pytest.raises(NotImplementedYetError) as e:
        todo("will be implemented soon")
    assert "will be implemented soon" in str(e)

from typing import Literal, assert_type

from .identity import identity


def test_identity() -> None:
    x: Literal[5] = 5
    assert_type(identity(x), Literal[5])

    y = object()
    assert identity(y) is y

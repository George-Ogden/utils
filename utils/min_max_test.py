from collections.abc import Callable
from typing import TYPE_CHECKING, Any, assert_type

import pytest

from .identity import identity
from .min_max import min_max


@pytest.mark.parametrize(
    "a, b, key, swap",
    [
        (3, 4, None, False),
        (4, 3, None, True),
        (3, 4, lambda x: -x, True),
        (4, 3, lambda x: -x, False),
        ("aaa", "bbb", len, False),
        ("bbb", "aaa", len, False),
        (3, 4, lambda _: 0, False),
        (4, 3, lambda _: 0, False),
    ],
)
def test_min_max(a: Any, b: Any, key: Callable[[Any], Any] | None, swap: bool) -> None:
    if swap:
        assert min_max(a, b, key=key) == (b, a)
    else:
        assert min_max(a, b, key=key) == (a, b)


@pytest.mark.typed
def test_min_max_type_hints_without_key() -> None:
    c = "abc"
    d = "def"
    assert_type(min_max(c, d), tuple[str, str])
    assert_type(min_max(c, d, key=None), tuple[str, str])
    assert_type(min_max(c, d, key=len), tuple[str, str])

    if TYPE_CHECKING:
        min_max(c, d, key=set.__len__)  # type: ignore
        min_max(c, d, key=dict.fromkeys)  # type: ignore


@pytest.mark.typed
def test_min_max_type_hints_with_key() -> None:
    a = {3: "c", 4: "d", 5: "e"}
    b = {3: "c", 4: "d"}
    assert_type(min_max(a, b, key=len), tuple[dict[int, str], dict[int, str]])

    if TYPE_CHECKING:
        min_max(a, b, key=None)  # type: ignore
        min_max(a, b)  # type: ignore
        min_max(a, b, key=identity)  # type: ignore
        min_max(a, b, len)  # type:ignore

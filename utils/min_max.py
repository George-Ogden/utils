from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, overload

from .identity import identity

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT


@overload
def min_max[T: SupportsDunderLT](a: T, b: T, key: None = None) -> tuple[T, T]: ...
@overload
def min_max[T, U: SupportsDunderLT](a: T, b: T, key: Callable[[T], U]) -> tuple[T, T]: ...


def min_max(a: Any, b: Any, key: Callable[[Any], Any] | None = None) -> tuple[Any, Any]:
    if key is None:
        key = identity
    if key(b) < key(a):
        return b, a
    return a, b

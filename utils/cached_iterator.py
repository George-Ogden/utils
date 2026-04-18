from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
import functools
from typing import Final

from .compose import compose

_CACHED_ITERATOR_TYPE: Final[type[tuple]] = tuple


def cached_iterator[T](fn: Callable[..., Iterable[T]]) -> functools._lru_cache_wrapper[Sequence[T]]:
    """
    Cache an iterator by storing all the resulting elements as a tuple.
    This works as on plain functions, or as an instance method, `property`, `classmethod` or other descriptor.

    Example use:
    ```python
    from typing import Generator
    from utils import cached_iterator

    @cached_iterator
    def squares(n: int) -> Generator[int]:
        for i in range(1, n + 1):
            yield i ** 2

    assert squares(5) == (1, 4, 9, 16, 25)
    assert squares(5) is squares(5) # cached
    ```
    """
    return functools.lru_cache(typed=True)(compose(_CACHED_ITERATOR_TYPE, fn))

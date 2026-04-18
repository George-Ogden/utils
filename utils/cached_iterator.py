from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
import functools
from typing import Final

from .compose import compose

_CACHED_ITERATOR_TYPE: Final[type[tuple]] = tuple


def cached_iterator[**P, T](
    fn: Callable[P, Iterable[T]],
) -> functools._lru_cache_wrapper[Sequence[T]]:
    return functools.lru_cache(typed=True)(compose(_CACHED_ITERATOR_TYPE, fn))

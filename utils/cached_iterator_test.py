from collections.abc import Iterator
from dataclasses import dataclass
import math

from . import cached_iterator
from .cached_iterator import _CACHED_ITERATOR_TYPE


def test_cached_iterator_existing_fn() -> None:
    cached_range_fn = cached_iterator(range)
    original_range = cached_range_fn(5)
    assert original_range == _CACHED_ITERATOR_TYPE([0, 1, 2, 3, 4])
    new_range = cached_range_fn(5)
    assert original_range is new_range
    assert new_range == _CACHED_ITERATOR_TYPE([0, 1, 2, 3, 4])


def test_cached_iterator_new_fn() -> None:
    @cached_iterator
    def yield_squares(n: int) -> Iterator[int]:
        for i in range(n + 1):
            yield i**2

    assert yield_squares(4) == _CACHED_ITERATOR_TYPE([0, 1, 4, 9, 16])
    assert yield_squares(3) == _CACHED_ITERATOR_TYPE([0, 1, 4, 9])
    assert yield_squares(100) is yield_squares(100)


def test_cached_iterator_instance_method() -> None:

    @dataclass(frozen=True)
    class Between:
        lower_bound: int | float

        @cached_iterator
        def and_(self, upper_bound: int | float) -> Iterator[int]:
            yield from range(math.ceil(self.lower_bound), math.floor(upper_bound) + 1)

    from_3 = Between(3)
    assert from_3.and_(4) == _CACHED_ITERATOR_TYPE([3, 4])
    assert from_3.and_(5) == _CACHED_ITERATOR_TYPE([3, 4, 5])

    assert Between(5).and_(10) is Between(5).and_(10)
    assert Between(5).and_(10) is not Between(5.0).and_(10.0)


def test_cached_iterator_class_method() -> None:

    @dataclass(frozen=True)
    class AlternateNumbers:
        @classmethod
        @cached_iterator
        def between(cls, lower_bound: int, upper_bound: int) -> Iterator[int]:
            yield from range(lower_bound, upper_bound + 1, 2)

    assert AlternateNumbers.between(3, 10) == _CACHED_ITERATOR_TYPE([3, 5, 7, 9])
    assert AlternateNumbers.between(4, 8) == _CACHED_ITERATOR_TYPE([4, 6, 8])

    assert AlternateNumbers.between(1, 500) is AlternateNumbers.between(1, 500)


def test_cached_iterator_property() -> None:

    @dataclass(frozen=True)
    class UpTo:
        bound: int

        @property
        @cached_iterator
        def naturals(self) -> Iterator[int]:
            yield from range(self.bound + 1)

    up_to_4 = UpTo(4)
    assert up_to_4.naturals == _CACHED_ITERATOR_TYPE([0, 1, 2, 3, 4])

    assert UpTo(6).naturals == UpTo(6).naturals
    assert UpTo(9).naturals is UpTo(9).naturals

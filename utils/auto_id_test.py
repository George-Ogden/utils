from dataclasses import dataclass
from typing import Self

from . import AutoId
from .plugins.pytest_plugin import reset_global_id as reset_global_id


def test_auto_id_next() -> None:
    @dataclass(frozen=True)
    class AutoIdSubclass(AutoId):
        id: int

        @classmethod
        def next(cls) -> Self:
            return cls(cls.next_id())

    assert AutoIdSubclass.next_id() == 0
    assert AutoIdSubclass.next() == AutoIdSubclass(1)

    assert AutoId._global_id == 0  # type:ignore[misc]


class AutoIdDirectSubclass(AutoId): ...


class SharedAutoIdIndirectSubclass(AutoId): ...


def test_auto_id_reset_between_tests_1() -> None:
    assert SharedAutoIdIndirectSubclass.next_id() == 0


def test_auto_id_reset_between_tests_2() -> None:
    assert SharedAutoIdIndirectSubclass.next_id() == 0


def test_auto_id_reset_non_zero() -> None:
    @dataclass(frozen=True)
    class AutoIdCustomSubclass(AutoId[str]):
        @classmethod
        def _id_default_value(cls) -> str:
            return ""

        @classmethod
        def _increment_id(cls, id: str) -> str:
            return id + "1"

    assert AutoIdCustomSubclass._global_id == ""  # type:ignore[misc]
    assert AutoIdCustomSubclass.next_id() == ""
    assert AutoIdCustomSubclass.next_id() == "1"
    assert AutoIdCustomSubclass.next_id() == "11"

    AutoIdCustomSubclass.reset_global_id()
    assert AutoIdCustomSubclass._global_id == ""  # type:ignore[misc]
    assert AutoIdCustomSubclass.next_id() == ""
    assert AutoIdCustomSubclass.next_id() == "1"

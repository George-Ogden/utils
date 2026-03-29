from __future__ import annotations

from collections.abc import Iterable
import inspect
from typing import TYPE_CHECKING, final

import pytest

if TYPE_CHECKING:
    from mypy_pytest_plugin_types import ParameterSet


def cases[Self: type](cls: Self) -> Iterable[ParameterSet[Self]]:
    for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
        if name != "cases" and not name.startswith("_"):
            yield pytest.param(method(), id=name)


def test_case[T: type](cls: T) -> T:
    cls.cases = classmethod(cases)  # type: ignore [attr-defined]
    return final(cls)


test_case.__test__ = False

import inspect
from typing import TYPE_CHECKING, final

import pytest

if TYPE_CHECKING:
    from mypy_pytest_plugin_types import ParameterSet


def cases[Self: type](cls: Self) -> list["ParameterSet[Self]"]:
    for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
        if name != "cases" and not name.startswith("_"):
            marks = pytest.mark.xfail(strict=True) if name.endswith("xfail") else ()
            yield pytest.param(method(), id=name, marks=marks)


@pytest.mark.typed
def test_case[T: type](cls: T) -> T:
    if not hasattr(cls, "cases"):
        cls.cases = classmethod(cases)  # type: ignore [attr-defined]
    return final(cls)


test_case.__test__ = False

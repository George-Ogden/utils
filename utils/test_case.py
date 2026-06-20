import inspect
from typing import TYPE_CHECKING, final

import pytest

if TYPE_CHECKING:
    from _pytest.mark.structures import _XfailMarkDecorator
    from mypy_pytest_plugin_types import ParameterSet


def _marks_for(name: str) -> tuple[()] | type["_XfailMarkDecorator"]:
    if name.endswith("xfail"):
        return pytest.mark.xfail(strict=True)
    return ()


def cases[Self: type](cls: Self) -> list["ParameterSet[Self]"]:
    return [
        pytest.param(method(), id=name, marks=_marks_for(name))
        for name, method in inspect.getmembers(cls, predicate=inspect.ismethod)
        if name != "cases" and not name.startswith("_")
    ]


@pytest.mark.typed
def test_case[T: type](cls: T) -> T:
    if not hasattr(cls, "cases"):
        cls.cases = classmethod(cases)  # type: ignore [attr-defined]
    return final(cls)


test_case.__test__ = False

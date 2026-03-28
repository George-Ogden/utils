import contextlib
from typing import Any, overload

import pytest


@overload
def check_for_errors[E: BaseException](expected: type[E]) -> pytest.RaisesExc[E]: ...


@overload
def check_for_errors(expected: Any) -> contextlib.nullcontext | pytest.RaisesExc[Exception]: ...


def check_for_errors(expected: Any) -> Any:
    return (
        pytest.raises(expected)
        if isinstance(expected, type) and issubclass(expected, BaseException)
        else contextlib.nullcontext()
    )


@overload
def check_for_assertion_errors(expected: None) -> pytest.RaisesExc[AssertionError]: ...


@overload
def check_for_assertion_errors(
    expected: Any,
) -> contextlib.nullcontext | pytest.RaisesExc[AssertionError]: ...


def check_for_assertion_errors(expected: Any) -> Any:
    return check_for_errors(AssertionError if expected is None else expected)

import contextlib
from typing import Any, overload

import pytest


@overload
def check_for_errors[E: BaseException](expected: type[E]) -> pytest.RaisesExc[E]: ...


@overload
def check_for_errors(expected: Any) -> contextlib.nullcontext | pytest.RaisesExc[BaseException]: ...


def check_for_errors(expected: Any) -> Any:
    """
    Expect that a specific exception is raised when its type is passed in.
    Otherwise, do nothing.
    It is used in parametrized testing to check that an error case is caught correctly.
    For example:
    ```python
    expected: IndexError | str
    with check_for_errors(expected):
        assert get_index(idx) == expected
    ```
    This will fail if an index that should be out of bounds returns a value;
    a returned value incorrect; or
    a valid index raises an IndexError.
    """
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
    """
    Expect that an `AssertionError` is raised if the expected value is `None.`
    Otherwise, do nothing.
    It is used in parametrized testing to check that an assert correctly catches an error case.
    This requires special attention in some cases.
    This example may pass in all cases if no error is raised:
    ```python
    with check_for_assertion_errors(expected):
        assert fn(value) == expected
    ```
    So it can be written instead as:
    ```python
    with check_for_assertion_errors(expected):
        result = fn(value)
    with contextlib.suppress(NameError):
        assert result == expected
    ```
    The exact pattern for this is still evolving.
    """
    return check_for_errors(AssertionError if expected is None else expected)

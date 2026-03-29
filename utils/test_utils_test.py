from typing import Any, assert_type

import pytest

from .test_utils import check_for_assertion_errors, check_for_errors


@pytest.mark.xfail(strict=True)
def test_check_for_errors_no_error() -> None:
    with check_for_errors(ValueError) as e:
        assert_type(e, pytest.ExceptionInfo[ValueError])
        assert True


@pytest.mark.typed
def test_check_for_errors_correct_error() -> None:
    with check_for_errors(ValueError) as e:
        assert_type(e, pytest.ExceptionInfo[ValueError])
        float("abc")


@pytest.mark.xfail(strict=True, raises=ValueError)
def test_check_for_errors_incorrect_error() -> None:
    with check_for_errors(IndexError) as e:
        assert_type(e, pytest.ExceptionInfo[IndexError])
        float("abc")


@pytest.mark.typed
def test_check_for_errors_all_fine() -> None:
    with check_for_errors(None) as e:
        assert_type(e, Any | pytest.ExceptionInfo[BaseException])
        assert True


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_check_for_errors_not_fine() -> None:
    with check_for_errors(None) as e:
        assert_type(e, Any | pytest.ExceptionInfo[BaseException])
        raise AssertionError()


@pytest.mark.xfail(strict=True)
def test_check_for_assertion_errors_no_error() -> None:
    with check_for_assertion_errors(None) as e:
        assert_type(e, pytest.ExceptionInfo[AssertionError])
        assert True


@pytest.mark.typed
def test_check_for_assertion_errors_assertion_error() -> None:
    with check_for_assertion_errors(None) as e:
        assert_type(e, pytest.ExceptionInfo[AssertionError])
        raise AssertionError()


@pytest.mark.typed
def test_check_for_assertion_errors_all_fine() -> None:
    with check_for_assertion_errors(1) as e:
        assert_type(e, Any | pytest.ExceptionInfo[AssertionError])
        assert True


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_check_for_assertion_errors_not_fine() -> None:
    with check_for_assertion_errors(1) as e:
        assert_type(e, Any | pytest.ExceptionInfo[AssertionError])
        raise AssertionError()

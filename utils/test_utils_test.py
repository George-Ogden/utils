import pytest

from .test_utils import check_for_assertion_errors, check_for_errors


@pytest.mark.xfail(strict=True)
def test_check_for_errors_no_error() -> None:
    with check_for_errors(ValueError):
        assert True


@pytest.mark.typed
def test_check_for_errors_correct_error() -> None:
    with check_for_errors(ValueError):
        float("abc")


@pytest.mark.xfail(strict=True, raises=ValueError)
def test_check_for_errors_incorrect_error() -> None:
    with check_for_errors(IndexError):
        float("abc")


@pytest.mark.typed
def test_check_for_errors_all_fine() -> None:
    with check_for_errors(None):
        assert True


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_check_for_errors_not_fine() -> None:
    with check_for_errors(None):
        raise AssertionError()


@pytest.mark.xfail(strict=True)
def test_check_for_assertion_errors_no_error() -> None:
    with check_for_assertion_errors(None):
        assert True


@pytest.mark.typed
def test_check_for_assertion_errors_assertion_error() -> None:
    with check_for_assertion_errors(None):
        raise AssertionError()


@pytest.mark.typed
def test_check_for_assertion_errors_all_fine() -> None:
    with check_for_assertion_errors(1):
        assert True


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_check_for_assertion_errors_not_fine() -> None:
    with check_for_assertion_errors(1):
        raise AssertionError()

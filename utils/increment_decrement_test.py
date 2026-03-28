import pytest

from .decrement import decrement
from .increment import increment


@pytest.mark.parametrize("lower, upper", [(0, 1), (-1, 0), (10, 11), (50.0, 51.0), (-100.0, -99.0)])
def test_increment_decrement(
    lower: int | float, upper: int | float, subtests: pytest.Subtests
) -> None:
    with subtests.test("increment"):
        result = increment(lower)
        assert result == upper
        assert type(result) is type(upper)

    with subtests.test("decrement"):
        result = decrement(upper)
        assert result == lower
        assert type(result) is type(lower)

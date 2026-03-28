import pytest

from .round import round


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (10, 10),
        (-5.0, -5),
        (2.6, 3),
        (2.4, 2),
        (-1.1, -1),
        (2.5, 3),
        (-2.5, -2),
        (4.5 - 1e-9, 4),
        (-4.5 + 1e-9, -4),
        (1e9 + 0.5, 10**9 + 1),
    ],
)
def test_round(value: float, expected: int) -> None:
    assert round(value) == expected

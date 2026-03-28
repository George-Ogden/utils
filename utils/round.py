import math


def round(x: int | float, /) -> int:
    """
    Round the value to the nearest integer.
    When n is a natural number,
    - `n + 0.5` rounds to `n + 1`
    - `-n - 0.5` rounds to `-n`
    For example:
    ```
    >>> from utils import round
    >>> round(4.5)
    5
    >>> round(-4.5)
    4
    >>> round(0.5)
    1
    >>> round(-0.5)
    0
    ```
    You must import this function as it has different behavior to the `builtins.round`.
    """
    return math.floor(x + 0.5)

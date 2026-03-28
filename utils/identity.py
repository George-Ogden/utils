from extra_types.types import Unmodified


def identity[T](x: T, /) -> Unmodified[T]:
    """Return the value unchanged."""
    return x

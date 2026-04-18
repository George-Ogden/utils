from collections.abc import Callable


def compose[**P, T, U](f: Callable[[T], U], g: Callable[P, T], /) -> Callable[P, U]:
    """Combine functions `f` and `g` to `f.g` where `f.g(x) = f(g(x))`."""
    return lambda *args, **kwargs: f(g(*args, **kwargs))

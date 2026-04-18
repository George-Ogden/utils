from typing import NoReturn

from .errors import NotImplementedYetError


def unimplemented(*args: object) -> NoReturn:
    """
    Raises a `NotImplemented` error.
    Any additional args will be passed into the error.
    """
    raise NotImplementedError(*args)


def todo(*args: object) -> NoReturn:
    """
    Raises a `NotImplementedYet` error, which is a subclass of a `NotImplementedError`.
    Any additional args will be passed into the error.
    """
    raise NotImplementedYetError(*args)

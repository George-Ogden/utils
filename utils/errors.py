from typing import NoReturn


class NotImplementedYetError(NotImplementedError): ...


class UnreachableError(AssertionError): ...


def unimplemented(*args: object) -> NoReturn:
    """
    Raises a `NotImplemented` error.
    Any additional args will be passed into the error.
    """
    raise NotImplementedError(*args)


def todo(*args: object) -> NoReturn:
    """
    Raises a `NotImplementedYetError`, which is a subclass of a `NotImplementedError`.
    Any additional args will be passed into the error.
    """
    raise NotImplementedYetError(*args)


def unreachable(*args: object) -> NoReturn:
    """
    Raises an `UnreachableError`, which is a subclass of an `AssertionError`.
    Any additional args will be passed into the error.
    """
    raise UnreachableError(*args)

from typing import NoReturn

from .errors import NotImplementedYetError


def unimplemented(*args: object) -> NoReturn:
    raise NotImplementedError(*args)


def todo(*args: object) -> NoReturn:
    raise NotImplementedYetError(*args)

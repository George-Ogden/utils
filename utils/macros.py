from typing import NoReturn


def unimplemented(*args: object) -> NoReturn:
    raise NotImplementedError(*args)

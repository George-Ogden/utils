from typing import ClassVar, cast

from extra_types.types import Nat


class AutoId[T = Nat]:
    _global_id: ClassVar[T] = cast(T, 0)

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        cls.reset_global_id()

    @classmethod
    def _increment_global_id(cls) -> None:
        cls._global_id += 1  # type:ignore

    @classmethod
    def next_id(cls) -> T:
        id = cls._global_id
        cls._increment_global_id()
        return id

    @classmethod
    def _global_id_default_value(cls) -> T:
        return cast(T, 0)

    @classmethod
    def reset_global_id(cls) -> None:
        cls._global_id = cls._global_id_default_value()

    @classmethod
    def _reset_all_global_ids(cls) -> None:
        cls.reset_global_id()
        for subclass in cls.__subclasses__():
            subclass._reset_all_global_ids()

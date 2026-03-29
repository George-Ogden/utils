from collections.abc import Callable

from mypy.nodes import MypyFile
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import add_method_to_class
from mypy.types import Instance, TypeVarType


class TestCasePlugin(Plugin):
    def get_additional_deps(self, file: MypyFile) -> list[tuple[int, str, int]]:
        return [self.module_to_dep("typing"), self.module_to_dep("mypy_pytest_plugin_types")]

    @classmethod
    def module_to_dep(cls, module: str) -> tuple[int, str, int]:
        return (10, module, -1)

    def get_class_decorator_hook_2(self, fullname: str) -> Callable[[ClassDefContext], bool] | None:
        if fullname == "utils.test_utils.test_case.test_case":
            return self.test_case_decorator_hook
        return None

    @classmethod
    def test_case_decorator_hook(cls, ctx: ClassDefContext) -> bool:
        add_method_to_class(
            ctx.api,
            ctx.cls,
            name="cases",
            args=[],
            return_type=cls.cases_return_type(ctx),
            is_classmethod=True,
        )
        ctx.cls.info.is_final = True
        return True

    @classmethod
    def cases_return_type(cls, ctx: ClassDefContext) -> Instance:
        return Instance(
            ctx.api.named_type("typing.Iterable").type,
            [
                Instance(
                    ctx.api.named_type("mypy_pytest_plugin_types.ParameterSet").type,
                    [cls.self_type(ctx)],
                )
            ],
        )

    @classmethod
    def self_type(cls, ctx: ClassDefContext) -> TypeVarType:
        self_type = ctx.cls.info.self_type
        assert self_type is not None
        return self_type


def plugin(version: str) -> type[TestCasePlugin]:
    return TestCasePlugin

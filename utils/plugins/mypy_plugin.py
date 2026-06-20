from collections.abc import Callable
from typing import Final

from mypy.errorcodes import ErrorCode
from mypy.nodes import ArgKind, Decorator, FuncDef, MypyFile, TypeInfo
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import SemanticAnalyzerPluginInterface, add_method_to_class
from mypy.subtypes import is_subtype
from mypy.types import AnyType, CallableType, Instance, TypeOfAny, TypeType, TypeVarType

TEST_CASE_ERROR_CODE: Final[ErrorCode] = ErrorCode(
    "test-case",
    "Class method used with test case decorator should return self.",
    category="TestCase",
)


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
        target_cls = ctx.cls
        type_info = target_cls.info
        if "cases" not in type_info.names:
            cls.analyze_type_info(ctx)
        type_info.is_final = True
        return True

    @classmethod
    def analyze_type_info(cls, ctx: ClassDefContext) -> None:
        target_cls = ctx.cls
        cls.check_class_methods(ctx)

        add_method_to_class(
            ctx.api,
            target_cls,
            name="cases",
            args=[],
            return_type=cls.cases_return_type(ctx),
            is_classmethod=True,
        )

    @classmethod
    def check_class_methods(cls, ctx: ClassDefContext) -> None:
        target_cls = ctx.cls
        type_info = target_cls.info

        for name, entry in type_info.names.items():
            if not name.startswith("_") and isinstance(entry.node, FuncDef | Decorator):
                cls.check_method(name, entry.node, type_info, ctx.api)

    @classmethod
    def check_method(
        cls,
        name: str,
        node: FuncDef | Decorator,
        type_info: TypeInfo,
        sem_anal: SemanticAnalyzerPluginInterface,
    ) -> None:
        func = cls.get_func(node)
        if func.is_class:
            cls.check_class_method(name, node, type_info, sem_anal)

    @classmethod
    def check_class_method(
        cls,
        name: str,
        node: FuncDef | Decorator,
        type_info: TypeInfo,
        sem_anal: SemanticAnalyzerPluginInterface,
    ) -> None:
        if node.type is not None and not is_subtype(
            node.type, cls.expected_class_method_type(type_info, sem_anal)
        ):
            sem_anal.fail(
                msg=f"`{type_info.name}.{name}` should return Self when being used with the `@test_case` decorator.",
                ctx=cls.get_func(node),
                code=TEST_CASE_ERROR_CODE,
            )

    @classmethod
    def get_func(cls, node: FuncDef | Decorator) -> FuncDef:
        return node if isinstance(node, FuncDef) else node.func

    @classmethod
    def expected_class_method_type(
        cls, type_info: TypeInfo, sem_anal: SemanticAnalyzerPluginInterface
    ) -> CallableType:
        loose_self_type = cls.loose_self_type(type_info)
        self_type = type_info.self_type

        return CallableType(
            arg_types=[TypeType(self_type)],
            arg_kinds=[ArgKind.ARG_POS],
            arg_names=[None],
            ret_type=loose_self_type,
            fallback=sem_anal.named_type("builtins.function"),
        )

    @classmethod
    def loose_self_type(cls, type_info: TypeInfo) -> Instance:
        return Instance(
            type_info, [AnyType(TypeOfAny.from_omitted_generics)] * len(type_info.defn.type_vars)
        )

    @classmethod
    def cases_return_type(cls, ctx: ClassDefContext) -> Instance:
        return Instance(
            ctx.api.named_type("builtins.list").type,
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

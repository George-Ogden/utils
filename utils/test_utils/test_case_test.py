from typing import NamedTuple, Self

import more_itertools as mit
import pytest

from .test_case import test_case


@test_case
class TestCaseSample(NamedTuple):
    value: float
    should_work: bool

    @classmethod
    def positive_value(cls) -> Self:
        return cls(1.0, True)

    @classmethod
    def negative_value(cls) -> Self:
        return cls(-1.0, True)

    @classmethod
    def _invalid_value(cls) -> Self:
        return cls(float("nan"), False)


TestCaseSample.__test__ = False  # type: ignore[attr-defined]


@pytest.mark.parametrize("case", TestCaseSample.cases())
def test_test_case_sample_cases(case: TestCaseSample) -> None:
    assert isinstance(case, TestCaseSample)
    assert case.should_work


def test_test_case_sample_length() -> None:
    assert mit.ilen(TestCaseSample.cases()) == 2
    assert mit.all_unique(TestCaseSample.cases())

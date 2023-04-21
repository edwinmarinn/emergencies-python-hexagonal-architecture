import pytest

from contexts.shared.infrastructure.bus.callable_first_parameter_extractor import (
    CallableFirstParameterExtractor,
)


class Parameter:
    pass


class ClassWithCallableParameter:
    def __call__(self, parameter: Parameter):
        pass


class ClassWithoutCallable:
    pass


class ClassWithoutCallableParameter:
    def __call__(self):
        pass


class ClassWithoutCallableParameterAnnotation:
    def __call__(self, parameter):
        pass


class TestCallableFirstParameterExtractor:
    @pytest.mark.parametrize("value", [ClassWithCallableParameter()])
    def test_should_extract_the_parameter(self, value):
        answer = CallableFirstParameterExtractor.extract(value)
        assert answer == Parameter

    @pytest.mark.parametrize(
        "value",
        [
            ClassWithoutCallable(),
            ClassWithoutCallableParameter(),
            ClassWithoutCallableParameterAnnotation(),
        ],
    )
    def test_should_not_extract_the_parameter_because_no_exist(self, value):
        answer = CallableFirstParameterExtractor.extract(value)
        assert answer is None

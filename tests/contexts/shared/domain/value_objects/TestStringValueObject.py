import pytest

from contexts.shared.domain.value_objects import StringValueObject


class TestStringValueObject:
    @pytest.mark.parametrize(
        "value",
        ["hi", "hello"],
    )
    def test_should_instantiate_from_str(self, value):
        number = StringValueObject(value)
        assert number.value == value

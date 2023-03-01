import pytest

from contexts.shared.domain.value_objects import IntValueObject


class TestIntValueObject:
    @pytest.mark.parametrize(
        "value",
        [-20, -15, 0, 15, 20],
    )
    def test_should_instantiate_from_int(self, value):
        number = IntValueObject(value)
        assert number.value == value

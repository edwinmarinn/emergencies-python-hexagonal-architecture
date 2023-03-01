import pytest

from contexts.shared.domain.value_objects import PositiveIntValueObject


class TestPositiveIntValueObject:
    @pytest.mark.parametrize(
        "value",
        [0, 12, 434, 45435345435],
    )
    def test_should_instantiate_from_valid_int(self, value):
        positive_int = PositiveIntValueObject(value)
        assert positive_int.value == value

    @pytest.mark.parametrize("value", [-12, -434, -4543534])
    def test_should_fail_instantiate_from_negative_int(self, value):
        with pytest.raises(ValueError):
            PositiveIntValueObject(value)

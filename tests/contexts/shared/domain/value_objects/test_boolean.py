import pytest

from contexts.shared.domain.value_objects.boolean import Boolean


class TestBoolean:
    @pytest.mark.parametrize("value", [True, False])
    def test_should_instantiate_from_bool(self, value):
        number = Boolean(value)
        assert number.value == value

    @pytest.mark.parametrize("value", [1, 0, "1", "2"])
    def test_should_fail_instantiate_from_non_bool(self, value):
        with pytest.raises(TypeError):
            Boolean(value)

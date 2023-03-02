import pytest

from contexts.shared.domain.value_objects import String


class TestString:
    @pytest.mark.parametrize(
        "value",
        ["hi", "hello"],
    )
    def test_should_instantiate_from_str(self, value):
        number = String(value)
        assert number.value == value

    @pytest.mark.parametrize(
        "value",
        [1, 2, True],
    )
    def test_should_fail_instantiate_from_non_str(self, value):
        with pytest.raises(TypeError):
            String(value)

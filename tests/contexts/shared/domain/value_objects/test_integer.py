import pytest

from contexts.shared.domain.value_objects import Integer


class TestInteger:
    @pytest.mark.parametrize(
        "value",
        [-20, -15, 0, 15, 20],
    )
    def test_should_instantiate_from_int(self, value):
        number = Integer(value)
        assert number.value == value

    @pytest.mark.parametrize(
        "value",
        ["-20", "-15", "0", "15", "20"],
    )
    def test_should_fail_instantiate_from_str(self, value):
        with pytest.raises(TypeError):
            Integer(value)

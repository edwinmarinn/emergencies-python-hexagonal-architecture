import pytest

from contexts.incidentes.shared.domain.value_objects import Abscisa


class TestAbscisa:
    @pytest.mark.parametrize("value", [0, 100, 1000, 10500])
    def test_should_instantiate_from_valid_value(self, value):
        abscisa = Abscisa(value)
        assert abscisa.value == value

    @pytest.mark.parametrize("value", [-1, -100, -1000, -10500])
    def test_should_fail_instantiate_from_invalid_value(self, value):
        with pytest.raises(ValueError):
            Abscisa(value)

    @pytest.mark.parametrize(
        "value",
        [
            "K1+300",
            "k1+300",
            " k 1+300 ",
            " k 1+300.0 ",
            " k 1+300.1 ",
            " k 1+299.6 ",
            "1+300",
            " k 1+300,1 ",
            " k 1+299,6 ",
            "PR1+300",
            "PR 1+300",
            " PR 1+300 ",
        ],
    )
    def test_should_create_from_valid_string(self, value):
        abscisa = Abscisa.create(value)
        assert abscisa.value == 1300

    @pytest.mark.parametrize(
        "value",
        ["Hi", "hello", "12hello"],
    )
    def test_should_fail_create_from_invalid_string(self, value):
        with pytest.raises(ValueError):
            Abscisa.create(value)

    def test_should_create_from_valid_int(self):
        assert Abscisa.create(0).value == 0
        assert Abscisa.create(1300).value == 1300

    @pytest.mark.parametrize(
        "value",
        ["1300.0", "1300.2", "1299.6", "1299,6"],
    )
    def test_should_create_from_float_as_string(self, value):
        abscisa = Abscisa.create(value)
        assert abscisa.value == 1300

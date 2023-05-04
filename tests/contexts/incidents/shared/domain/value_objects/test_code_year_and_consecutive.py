import datetime

import pytest
import time_machine

from contexts.incidents.shared.domain.value_objects import CodeYearAndConsecutive

tz_bogota = datetime.timezone(-datetime.timedelta(hours=5), "America/Bogota")


class TestCodeYearAndConsecutive:
    @time_machine.travel(datetime.datetime(2021, 1, 5, 12, 0, 0, tzinfo=tz_bogota))
    def test_should_instantiate_from_valid_value(self):
        assert CodeYearAndConsecutive("2021.00001").value == "2021.00001"
        assert CodeYearAndConsecutive("2021.1").value == "2021.1"

    @pytest.mark.parametrize("value", ["dasdasd", "2021", "2021.", ".00001"])
    def test_should_fail_instantiate_from_invalid_value(self, value):
        with pytest.raises(ValueError):
            CodeYearAndConsecutive(value)

    @time_machine.travel(datetime.datetime(2021, 1, 5, 12, 0, 0, tzinfo=tz_bogota))
    def test_next_code_same_year(self):
        current_code = CodeYearAndConsecutive("2021.00001")
        next_code = current_code.next()
        assert next_code.value == "2021.00002"

        current_code = CodeYearAndConsecutive("2021.1")
        next_code = current_code.next()
        assert next_code.value == "2021.00002"

    @time_machine.travel(datetime.datetime(2022, 1, 1, 1, 0, 0, tzinfo=tz_bogota))
    def test_next_code_changing_year(self):
        current_code = CodeYearAndConsecutive("2021.02341")
        next_code = current_code.next()
        assert next_code.value == "2022.00001"

        current_code = CodeYearAndConsecutive("2021.02000")
        next_code = current_code.next()
        assert next_code.value == "2022.00001"

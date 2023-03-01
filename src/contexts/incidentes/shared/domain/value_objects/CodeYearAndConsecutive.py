import datetime
import re
from typing import Optional

from contexts.shared.domain.value_objects import ValueObject

tz_bogota = datetime.timezone(-datetime.timedelta(hours=5), "America/Bogota")

YEAR_SEQUENCE_REGEX = re.compile(r"^(\d{4})\.(\d+)$")


class CodeYearAndConsecutive(ValueObject[str]):
    def __init__(self, value: str):
        super().__init__(value)
        self._ensure_valid_code(value)

    @staticmethod
    def _ensure_valid_code(code: str):
        match = YEAR_SEQUENCE_REGEX.match(code)
        if not match:
            raise ValueError(f"{code} is not a valid code")
        year, counter = match.groups()
        year = int(year)
        counter = int(counter)

        if counter == 0:
            raise ValueError(f"{code} counter of sequence must be greater than zero")

        return year, counter

    @staticmethod
    def _generate_code(
        previous: Optional[str] = None,
        separator=".",
        zfill_number=5,
        timezone=tz_bogota,
    ) -> str:
        """
        Generate a sequence with format: yyyy.counter

        Example:
            2021.00001

        :param previous: previous year sequence, defaults to None
        :param separator: sequence separator, defaults to "."
        :param zfill_number: number of zeros to fill, defaults to 5
        :param timezone: time zone to use, defaults to tz_bogota
        :raises ValueError: error con previous sequence
        :return: next sequence
        """
        now = datetime.datetime.now().astimezone(timezone)

        if previous is None:
            year = now.year
            counter = 1
        else:
            year, counter = CodeYearAndConsecutive._ensure_valid_code(previous)
            if year == now.year:
                counter += 1
            else:
                year = now.year
                counter = 1

        counter_str = str(counter).zfill(zfill_number)
        return f"{year}{separator}{counter_str}"

    @classmethod
    def generate(cls) -> "CodeYearAndConsecutive":
        return cls(cls._generate_code())

    def next(self):
        return CodeYearAndConsecutive(self._generate_code(self.value))

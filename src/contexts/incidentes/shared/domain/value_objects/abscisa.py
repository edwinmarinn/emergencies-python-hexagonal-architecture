import re
from typing import Union, cast

from typing_extensions import Self

from contexts.shared.domain.value_objects import ValueObject

REGEX_ABSCISSA = re.compile(
    r"^\s*(?:K|PR)?\s*(\d{0,3})\+(\d{3}(\.\d+)?)\s*$", re.IGNORECASE
)
REGEX_INT = re.compile(r"^\s*(\d+)\s*$")
REGEX_FLOAT = re.compile(r"^\s*(\d+\.\d+)\s*$")


class Abscisa(ValueObject[int]):
    def _validate(self, value: int):
        self._ensure_positive_value(value)

    @staticmethod
    def _ensure_positive_value(value: int):
        if value < 0:
            raise ValueError("Value should be positive")

    @staticmethod
    def _create_primitive(abscissa_str: Union[str, int, float]) -> int:
        """
        Get the numerical value of an abscissa from a string
        Example:
        'K1+300' -> 1300
        'k1+300' -> 1300
        '1+300' -> 1300
        """
        if type(abscissa_str) == int:
            return cast(int, abscissa_str)

        if type(abscissa_str) == float:
            return round(cast(float, abscissa_str))

        if type(abscissa_str) == str:
            abscissa_str = abscissa_str.replace(",", ".")

        abscissa_str = cast(str, abscissa_str)
        match_int = REGEX_INT.match(abscissa_str)
        if match_int:
            return int(match_int.group(1))

        match_float = REGEX_FLOAT.match(abscissa_str)
        if match_float:
            return round(float(match_float.group(1)))

        match_abscissa = REGEX_ABSCISSA.match(abscissa_str)
        if match_abscissa:
            kilometers, meters = match_abscissa.group(1, 2)
            return int(kilometers) * 1000 + round(float(meters))

        raise ValueError(f"{abscissa_str} is not a valid abscisa")

    @classmethod
    def create(cls, value: Union[str, int, float]) -> Self:
        return cls(cls._create_primitive(value))

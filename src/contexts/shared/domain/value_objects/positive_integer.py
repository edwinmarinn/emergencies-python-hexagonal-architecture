from .value_object import ValueObject


class PositiveInteger(ValueObject[int]):
    def _validate(self, value: int):
        self._ensure_type(value)
        self._ensure_positive_value(value)

    @staticmethod
    def _ensure_type(value):
        if type(value) != int:
            raise TypeError("Value should be int")

    @staticmethod
    def _ensure_positive_value(value: int):
        if value < 0:
            raise ValueError("Value should be positive")

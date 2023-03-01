from .ValueObject import ValueObject


class PositiveIntValueObject(ValueObject[int]):
    def __init__(self, value: int):
        super().__init__(value)
        self._ensure_positive_value(value)

    @staticmethod
    def _ensure_positive_value(value: int):
        if value < 0:
            raise ValueError("Value should be positive")

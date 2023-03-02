from .value_object import ValueObject


class Integer(ValueObject[int]):

    def _validate(self, value: int):
        self._ensure_type(value)

    @staticmethod
    def _ensure_type(value):
        if type(value) != int:
            raise TypeError("Value should be int")

    def __str__(self) -> str:
        return str(self.value)

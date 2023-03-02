from .value_object import ValueObject


class Boolean(ValueObject[bool]):
    def _validate(self, value: bool):
        self._ensure_type(value)

    @staticmethod
    def _ensure_type(value):
        if type(value) != bool:
            raise TypeError("Value should be bool")

from .value_object import ValueObject


class String(ValueObject[str]):

    def _validate(self, value: str):
        self._ensure_type(value)

    @staticmethod
    def _ensure_type(value):
        if type(value) != str:
            raise TypeError("Value should be str")

    def __str__(self) -> str:
        return self.value

from .ValueObject import ValueObject


class IntValueObject(ValueObject[int]):
    def __str__(self) -> str:
        return str(self.value)

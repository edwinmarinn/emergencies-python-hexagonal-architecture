from .ValueObject import ValueObject


class StringValueObject(ValueObject[str]):
    def __str__(self) -> str:
        return self.value

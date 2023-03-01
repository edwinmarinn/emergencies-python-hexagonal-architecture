from domain.shared.value_objects import ValueObject


class IntValueObject(ValueObject[int]):
    def __str__(self) -> str:
        return str(self.value)

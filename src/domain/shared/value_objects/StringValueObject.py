from domain.shared.value_objects.ValueObject import ValueObject


class StringValueObject(ValueObject[str]):
    def __str__(self) -> str:
        return self.value

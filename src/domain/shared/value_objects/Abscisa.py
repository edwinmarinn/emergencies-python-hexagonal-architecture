from domain.shared.value_objects import ValueObject


class Abscisa(ValueObject[int]):
    def __int__(self, value: int):
        super().__init__(value)
        self._ensure_valid_abscisa(value)

    @staticmethod
    def _ensure_valid_abscisa(abscisa: int):
        if abscisa < 0:
            raise ValueError(f"{abscisa} should be greeter than cero")

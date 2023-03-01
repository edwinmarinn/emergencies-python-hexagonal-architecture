import uuid as core_uuid

from .ValueObject import ValueObject


class Uuid(ValueObject[str]):
    VERSION = 4

    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.__ensure_is_valid_uuid(value)

    @classmethod
    def random(cls):
        return cls(str(core_uuid.uuid4()))

    def __ensure_is_valid_uuid(self, _id: str) -> None:
        core_uuid.UUID(_id, version=self.VERSION)

    def __str__(self) -> str:
        return self.value

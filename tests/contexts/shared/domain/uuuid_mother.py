import uuid


class UuidMother:
    @staticmethod
    def random():
        return str(uuid.uuid4())

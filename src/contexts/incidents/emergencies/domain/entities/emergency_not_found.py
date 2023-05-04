from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain import DomainError


class EmergencyNotFound(DomainError):
    def __init__(self, _id: EmergencyId):
        self._id = _id
        super().__init__()

    def error_code(self) -> str:
        return "emergency_not_found"

    def error_message(self) -> str:
        return f"The emergency {self._id.value} has not been found"

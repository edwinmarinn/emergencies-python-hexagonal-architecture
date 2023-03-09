from contexts.incidentes.emergencias.domain.value_objects import EmergenciaId
from contexts.shared.domain import DomainError


class EmergenciaNotFound(DomainError):
    def __init__(self, _id: EmergenciaId):
        self._id = _id
        super().__init__()

    def error_code(self) -> str:
        return "emergencia_not_found"

    def error_message(self) -> str:
        return f"The emergencia {self._id.value} has not been found"

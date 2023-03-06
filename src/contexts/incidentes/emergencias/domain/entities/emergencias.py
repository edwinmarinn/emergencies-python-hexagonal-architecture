from contexts.incidentes.emergencias.domain.entities import Emergencia
from contexts.shared.domain.collection import Collection


class Emergencias(Collection[Emergencia]):
    def type(self):
        return Emergencia

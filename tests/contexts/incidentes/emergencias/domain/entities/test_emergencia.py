from contexts.incidentes.emergencias.domain.entities import Emergencia
from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
    EmergenciaId,
)
from contexts.incidentes.shared.domain.value_objects import UsuarioId


class TestEmergencia:
    def test_should_instantiate(self):
        Emergencia(
            _id=EmergenciaId("bd904284-44f3-4e5b-815a-f5b5a7eb1cbf"),
            code=EmergenciaCode("2023.00001"),
            abscisa=EmergenciaAbscisa(500),
            usuario_id=UsuarioId("06daa82b-c733-4c8d-92cd-10074e2dd37a"),
        )

    def test_should_create(self):
        emergencia = Emergencia.create(
            _id=EmergenciaId("bd904284-44f3-4e5b-815a-f5b5a7eb1cbf"),
            code=EmergenciaCode("2023.00001"),
            abscisa=EmergenciaAbscisa(500),
            usuario_id=UsuarioId("06daa82b-c733-4c8d-92cd-10074e2dd37a"),
        )

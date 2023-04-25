from dependency_injector import containers, providers

from contexts.incidentes.emergencias.application.create import (
    CreateEmergenciaCommandHandler,
    EmergenciaCreator,
)
from contexts.incidentes.emergencias.application.find import (
    EmergenciaFinder,
    FindEmergenciaQueryHandler,
)
from contexts.incidentes.emergencias.application.list import (
    EmergenciasLister,
    ListEmergenciasQueryHandler,
)
from contexts.incidentes.emergencias.infrastructure.persistence.in_memory import (
    InMemoryEmergenciaRepository,
)
from contexts.shared.domain.bus.command import CommandBus
from contexts.shared.domain.bus.query import QueryBus
from contexts.shared.infrastructure.bus.command import InMemoryCommandBus
from contexts.shared.infrastructure.bus.event import InMemoryEventBus
from contexts.shared.infrastructure.bus.query import InMemoryQueryBus

emergencia_repository = InMemoryEmergenciaRepository()

event_bus = InMemoryEventBus()


def get_query_bus():
    return InMemoryQueryBus(
        [
            FindEmergenciaQueryHandler(EmergenciaFinder(emergencia_repository)),
            ListEmergenciasQueryHandler(EmergenciasLister(emergencia_repository)),
        ]
    )


def get_command_bus():
    return InMemoryCommandBus(
        [
            CreateEmergenciaCommandHandler(
                EmergenciaCreator(emergencia_repository, event_bus)
            )
        ]
    )


class InMemoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["apps.incidentes.backend.views"]
    )
    command_bus = providers.Singleton(get_command_bus)
    query_bus = providers.Singleton(get_query_bus)
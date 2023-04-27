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
from contexts.incidentes.emergencias_counter.application.increment import (
    IncrementEmergenciasCounterOnEmergenciaCreated,
)
from contexts.shared.infrastructure.bus.command import InMemoryCommandBus
from contexts.shared.infrastructure.bus.event import InMemoryEventBus
from contexts.shared.infrastructure.bus.event.rabbit_mq import (
    RabbitMqConfigurer,
    RabbitMqConnection,
    RabbitMqEventBus,
)
from contexts.shared.infrastructure.bus.query import InMemoryQueryBus

emergencia_repository = InMemoryEmergenciaRepository()


def get_in_memory_event_bus():
    return InMemoryEventBus([IncrementEmergenciasCounterOnEmergenciaCreated()])


def get_rabbit_mq_event_bus():
    connection = RabbitMqConnection({"url": "amqp://guest:guest@rabbitmq:5672/"})
    configurer = RabbitMqConfigurer(connection=connection)

    exchange_name = "incidentes-exchange"
    configurer.configure(
        exchange_name=exchange_name,
        subscribers=[IncrementEmergenciasCounterOnEmergenciaCreated()],
    )

    bus = RabbitMqEventBus(connection=connection, exchange_name=exchange_name)
    return bus


get_event_bus = get_rabbit_mq_event_bus


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
                EmergenciaCreator(emergencia_repository, get_event_bus())
            )
        ]
    )


class InMemoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["apps.incidentes.backend.views"]
    )
    command_bus = providers.Singleton(get_command_bus)
    query_bus = providers.Singleton(get_query_bus)

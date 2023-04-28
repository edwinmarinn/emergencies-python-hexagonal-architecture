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
    RabbitMqConnectionSettings,
    RabbitMqEventBus,
    RabbitMqQueueNameFormatter,
)
from contexts.shared.infrastructure.bus.event.rabbit_mq_async import (
    RabbitMqConfigurerAsync,
    RabbitMqConnectionAsync,
    RabbitMqEventBusAsync,
)
from contexts.shared.infrastructure.bus.query import InMemoryQueryBus

emergencia_repository = InMemoryEmergenciaRepository()

COMPANY_NAME = "devimed"

EXCHANGE_NAME = "devimed_incidentes"


def get_in_memory_event_bus():
    return InMemoryEventBus([IncrementEmergenciasCounterOnEmergenciaCreated()])


def get_rabbit_mq_connection_settings():
    return RabbitMqConnectionSettings(
        host="rabbitmq",
        port=5672,
        username="guest",
        password="guest",
        virtual_host="/",
    )


def get_rabbit_mq_event_bus_sync():
    connection = RabbitMqConnection(
        connection_settings=get_rabbit_mq_connection_settings()
    )
    configurer = RabbitMqConfigurer(
        connection=connection,
        queue_name_formatter=RabbitMqQueueNameFormatter(company=COMPANY_NAME),
    )

    configurer.configure(
        exchange_name=EXCHANGE_NAME,
        subscribers=[IncrementEmergenciasCounterOnEmergenciaCreated()],
    )

    bus = RabbitMqEventBus(connection=connection, exchange_name=EXCHANGE_NAME)
    return bus


async def get_rabbit_mq_event_bus_async():
    connection = RabbitMqConnectionAsync(
        connection_settings=get_rabbit_mq_connection_settings()
    )
    configurer = RabbitMqConfigurerAsync(
        connection=connection,
        queue_name_formatter=RabbitMqQueueNameFormatter(company=COMPANY_NAME),
    )

    await configurer.configure(
        exchange_name=EXCHANGE_NAME,
        subscribers=[IncrementEmergenciasCounterOnEmergenciaCreated()],
    )

    bus = RabbitMqEventBusAsync(connection=connection, exchange_name=EXCHANGE_NAME)
    return bus


get_event_bus = get_rabbit_mq_event_bus_async


def get_query_bus():
    return InMemoryQueryBus(
        [
            FindEmergenciaQueryHandler(EmergenciaFinder(emergencia_repository)),
            ListEmergenciasQueryHandler(EmergenciasLister(emergencia_repository)),
        ]
    )


async def get_command_bus():
    return InMemoryCommandBus(
        [
            CreateEmergenciaCommandHandler(
                EmergenciaCreator(emergencia_repository, await get_event_bus())
            )
        ]
    )


class InMemoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "apps.incidentes.backend_flask.views",
            "apps.incidentes.backend_fastapi.views",
        ]
    )
    command_bus = providers.Singleton(get_command_bus)
    query_bus = providers.Singleton(get_query_bus)

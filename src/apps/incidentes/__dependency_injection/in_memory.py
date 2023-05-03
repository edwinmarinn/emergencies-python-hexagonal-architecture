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
from contexts.incidentes.emergencias_counter.application.find import (
    EmergenciasCounterFinder,
    FindEmergenciasCounterQueryHandler,
)
from contexts.incidentes.emergencias_counter.application.increment import (
    EmergenciasCounterIncrementer,
    IncrementEmergenciasCounterOnEmergenciaCreated,
)
from contexts.incidentes.emergencias_counter.infraestructure.persistence import (
    InMemoryEmergenciasCounterRepository,
)
from contexts.incidentes.emergencias_counter_per_user.application.find import (
    EmergenciasCounterPerUserFinder,
    FindEmergenciasCounterPerUserQueryHandler,
)
from contexts.incidentes.emergencias_counter_per_user.application.increment import (
    EmergenciasCounterPerUserIncrementer,
    IncrementEmergenciasCounterPerUserOnEmergenciaCreated,
)
from contexts.incidentes.emergencias_counter_per_user.infraestructure.persistence import (
    InMemoryEmergenciasCounterPerUserRepository,
)
from contexts.shared.infrastructure.bus.command import InMemoryCommandBus
from contexts.shared.infrastructure.bus.event.rabbit_mq import (
    RabbitMqConfigurerAsync,
    RabbitMqConnectionAsync,
    RabbitMqConnectionSettings,
    RabbitMqEventBusAsync,
    RabbitMqQueueNameFormatter,
)
from contexts.shared.infrastructure.bus.query import InMemoryQueryBus


class InMemoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "apps.incidentes.backend_flask.views",
            "apps.incidentes.backend_fastapi.views",
        ]
    )

    company_name = providers.Object("devimed")

    exchange_name = providers.Object("devimed_incidentes")

    rabbit_mq_connection_settings = providers.Singleton(
        RabbitMqConnectionSettings,
        host="rabbitmq",
        port=5672,
        username="guest",
        password="guest",
        virtual_host="/",
    )

    queue_name_formatter = providers.Singleton(
        RabbitMqQueueNameFormatter, company=company_name
    )

    rabbit_mq_connection_async = providers.Singleton(
        RabbitMqConnectionAsync, connection_settings=rabbit_mq_connection_settings
    )

    rabbit_mq_connection_configurer = providers.Singleton(
        RabbitMqConfigurerAsync,
        connection=rabbit_mq_connection_async,
        queue_name_formatter=queue_name_formatter,
        message_retry_ttl=1000,
    )

    emergencia_repository = providers.Singleton(InMemoryEmergenciaRepository)
    emergencias_counter_repository = providers.Singleton(
        InMemoryEmergenciasCounterRepository
    )
    emergencias_counter_per_user_repository = providers.Singleton(
        InMemoryEmergenciasCounterPerUserRepository
    )

    query_bus = providers.Singleton(
        InMemoryQueryBus,
        providers.List(
            providers.Singleton(
                FindEmergenciaQueryHandler,
                finder=providers.Singleton(
                    EmergenciaFinder, repository=emergencia_repository
                ),
            ),
            providers.Singleton(
                ListEmergenciasQueryHandler,
                lister=providers.Singleton(
                    EmergenciasLister, repository=emergencia_repository
                ),
            ),
            providers.Singleton(
                FindEmergenciasCounterQueryHandler,
                finder=providers.Singleton(
                    EmergenciasCounterFinder, repository=emergencias_counter_repository
                ),
            ),
            providers.Singleton(
                FindEmergenciasCounterPerUserQueryHandler,
                finder=providers.Singleton(
                    EmergenciasCounterPerUserFinder,
                    repository=emergencias_counter_per_user_repository,
                ),
            ),
        ),
    )

    event_bus = providers.Singleton(
        RabbitMqEventBusAsync,
        connection=rabbit_mq_connection_async,
        exchange_name=exchange_name,
        queue_name_formatter=queue_name_formatter,
        max_retries=10,
    )

    command_bus = providers.Singleton(
        InMemoryCommandBus,
        providers.List(
            providers.Singleton(
                CreateEmergenciaCommandHandler,
                creator=providers.Singleton(
                    EmergenciaCreator, repository=emergencia_repository, bus=event_bus
                ),
            )
        ),
    )

    event_subscribers = providers.List(
        providers.Singleton(
            IncrementEmergenciasCounterOnEmergenciaCreated,
            incrementer=providers.Singleton(
                EmergenciasCounterIncrementer,
                repository=emergencias_counter_repository,
                bus=event_bus,
            ),
        ),
        providers.Singleton(
            IncrementEmergenciasCounterPerUserOnEmergenciaCreated,
            incrementer=providers.Singleton(
                EmergenciasCounterPerUserIncrementer,
                repository=emergencias_counter_per_user_repository,
                bus=event_bus,
            ),
        ),
    )

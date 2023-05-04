from dependency_injector import containers, providers

from contexts.incidents.emergencies.application.create import (
    CreateEmergencyCommandHandler,
    EmergencyCreator,
)
from contexts.incidents.emergencies.application.find import (
    EmergencyFinder,
    FindEmergencyQueryHandler,
)
from contexts.incidents.emergencies.application.list import (
    EmergenciesLister,
    ListEmergenciesQueryHandler,
)
from contexts.incidents.emergencies.infrastructure.persistence.in_memory import (
    InMemoryEmergencyRepository,
)
from contexts.incidents.emergencies_counter.application.find import (
    EmergenciesCounterFinder,
    FindEmergenciesCounterQueryHandler,
)
from contexts.incidents.emergencies_counter.application.increment import (
    EmergenciesCounterIncrementer,
    IncrementEmergenciesCounterOnEmergencyCreated,
)
from contexts.incidents.emergencies_counter.infraestructure.persistence import (
    InMemoryEmergenciesCounterRepository,
)
from contexts.incidents.emergencies_counter_per_user.application.find import (
    EmergenciesCounterPerUserFinder,
    FindEmergenciesCounterPerUserQueryHandler,
)
from contexts.incidents.emergencies_counter_per_user.application.increment import (
    EmergenciesCounterPerUserIncrementer,
    IncrementEmergenciesCounterPerUserOnEmergencyCreated,
)
from contexts.incidents.emergencies_counter_per_user.infraestructure.persistence import (
    InMemoryEmergenciesCounterPerUserRepository,
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
            "apps.incidents.backend_flask.views",
            "apps.incidents.backend_fastapi.views",
        ]
    )

    company_name = providers.Object("devimed")

    exchange_name = providers.Object("devimed_incidents")

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

    emergency_repository = providers.Singleton(InMemoryEmergencyRepository)
    emergencies_counter_repository = providers.Singleton(
        InMemoryEmergenciesCounterRepository
    )
    emergencies_counter_per_user_repository = providers.Singleton(
        InMemoryEmergenciesCounterPerUserRepository
    )

    query_bus = providers.Singleton(
        InMemoryQueryBus,
        providers.List(
            providers.Singleton(
                FindEmergencyQueryHandler,
                finder=providers.Singleton(
                    EmergencyFinder, repository=emergency_repository
                ),
            ),
            providers.Singleton(
                ListEmergenciesQueryHandler,
                lister=providers.Singleton(
                    EmergenciesLister, repository=emergency_repository
                ),
            ),
            providers.Singleton(
                FindEmergenciesCounterQueryHandler,
                finder=providers.Singleton(
                    EmergenciesCounterFinder, repository=emergencies_counter_repository
                ),
            ),
            providers.Singleton(
                FindEmergenciesCounterPerUserQueryHandler,
                finder=providers.Singleton(
                    EmergenciesCounterPerUserFinder,
                    repository=emergencies_counter_per_user_repository,
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
                CreateEmergencyCommandHandler,
                creator=providers.Singleton(
                    EmergencyCreator, repository=emergency_repository, bus=event_bus
                ),
            )
        ),
    )

    event_subscribers = providers.List(
        providers.Singleton(
            IncrementEmergenciesCounterOnEmergencyCreated,
            incrementer=providers.Singleton(
                EmergenciesCounterIncrementer,
                repository=emergencies_counter_repository,
                bus=event_bus,
            ),
        ),
        providers.Singleton(
            IncrementEmergenciesCounterPerUserOnEmergencyCreated,
            incrementer=providers.Singleton(
                EmergenciesCounterPerUserIncrementer,
                repository=emergencies_counter_per_user_repository,
                bus=event_bus,
            ),
        ),
    )
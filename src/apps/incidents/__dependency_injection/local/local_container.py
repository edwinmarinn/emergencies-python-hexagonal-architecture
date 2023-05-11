from pathlib import Path

from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

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
from contexts.incidents.emergencies.infrastructure.persistence.mongodb import (
    MongoDbEmergencyRepository,
)
from contexts.incidents.emergencies_counter.application.find import (
    EmergenciesCounterFinder,
    FindEmergenciesCounterQueryHandler,
)
from contexts.incidents.emergencies_counter.application.increment import (
    EmergenciesCounterIncrementer,
    IncrementEmergenciesCounterOnEmergencyCreated,
)
from contexts.incidents.emergencies_counter.infraestructure.persistence.mongodb import (
    MongodbEmergenciesCounterRepository,
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

CURRENT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = CURRENT_DIR.parent / "config.yml"


class LocalContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "apps.incidents.backend_flask.views",
            "apps.incidents.backend_fastapi.views",
        ]
    )

    config = providers.Configuration(yaml_files=[CONFIG_FILE], strict=True)

    company_name = providers.Object("company")

    exchange_name = providers.Object("company_incidents")

    rabbit_mq_connection_settings = providers.Singleton(
        RabbitMqConnectionSettings,
        host=config.rabbit_mq.host,
        port=config.rabbit_mq.port.as_int(),
        username=config.rabbit_mq.username,
        password=config.rabbit_mq.password,
        virtual_host=config.rabbit_mq.virtual_host,
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

    mongo_client = providers.Singleton(
        AsyncIOMotorClient, "mongodb://root:U9cUkvLF668u9gfT@mongo:27017/"
    )
    emergency_repository = providers.Singleton(
        MongoDbEmergencyRepository, client=mongo_client
    )
    emergencies_counter_repository = providers.Singleton(
        MongodbEmergenciesCounterRepository, client=mongo_client
    )

    # emergency_repository = providers.Singleton(InMemoryEmergencyRepository)
    # emergencies_counter_repository = providers.Singleton(
    #     InMemoryEmergenciesCounterRepository
    # )
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

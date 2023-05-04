from aiormq import AMQPConnectionError

from apps.incidents.__dependency_injection import Container
from contexts.shared.domain.utils.functions import retry_on_error


def configure_event_bus(container: Container, retries: int = 5, interval: int = 5):
    @retry_on_error(
        retries=retries, interval=interval, exception_class=AMQPConnectionError
    )
    async def configure_rabbit_mq():
        rabbit_mq_connection_configurer = container.rabbit_mq_connection_configurer()
        await rabbit_mq_connection_configurer.configure(
            exchange_name=container.exchange_name(),
            subscribers=container.event_subscribers(),
        )

    @retry_on_error(
        retries=retries, interval=interval, exception_class=AMQPConnectionError
    )
    async def configure_subscribers():
        event_bus = container.event_bus()
        await event_bus.add_subscribers(container.event_subscribers())

    async def configure():
        await configure_rabbit_mq()
        await configure_subscribers()

    return configure
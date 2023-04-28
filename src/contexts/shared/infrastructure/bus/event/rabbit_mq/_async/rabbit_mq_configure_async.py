from typing import Iterable

from aio_pika import ExchangeType

from contexts.shared.domain.bus.event import DomainEventSubscriber

from ..rabbit_mq_exchange_name_formatter import RabbitMqExchangeNameFormatter
from ..rabbit_mq_queue_name_formatter import RabbitMqQueueNameFormatter
from .rabbit_mq_connection_async import RabbitMqConnectionAsync


class RabbitMqConfigurerAsync:
    def __init__(
        self,
        connection: RabbitMqConnectionAsync,
        queue_name_formatter: RabbitMqQueueNameFormatter,
        message_retry_ttl=100,
    ) -> None:
        self._connection = connection
        self._queue_name_formatter = queue_name_formatter
        self._message_retry_ttl = message_retry_ttl

    async def configure(
        self, exchange_name: str, subscribers: Iterable[DomainEventSubscriber]
    ) -> None:
        await self._declare_exchanges(exchange_name)
        await self._declare_queues_for_subscribers(subscribers, exchange_name)

    async def _declare_exchanges(self, exchange_name: str) -> None:
        retry_exchange_name = RabbitMqExchangeNameFormatter.retry(exchange_name)
        dead_letter_exchange_name = RabbitMqExchangeNameFormatter.dead_letter(
            exchange_name
        )

        names = (exchange_name, retry_exchange_name, dead_letter_exchange_name)

        for name in names:
            await self._connection.exchange(
                name=name, type=ExchangeType.TOPIC, durable=True
            )

    async def _declare_queues_for_subscribers(
        self, subscribers: Iterable[DomainEventSubscriber], exchange_name: str
    ):
        retry_exchange_name = RabbitMqExchangeNameFormatter.retry(exchange_name)
        dead_letter_exchange_name = RabbitMqExchangeNameFormatter.dead_letter(
            exchange_name
        )

        for subscriber in subscribers:
            await self._queue_declarator(
                subscriber,
                exchange_name=exchange_name,
                retry_exchange_name=retry_exchange_name,
                dead_letter_exchange_name=dead_letter_exchange_name,
            )

    async def _queue_declarator(
        self,
        subscriber: DomainEventSubscriber,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
    ) -> None:
        queue_name = self._queue_name_formatter.format(subscriber)
        retry_queue_name = self._queue_name_formatter.format_retry(subscriber)
        dead_letter_queue_name = self._queue_name_formatter.format_dead_letter(
            subscriber
        )

        # Declare queues
        queue = await self._connection.queue(name=queue_name, durable=True)
        retry_queue = await self._connection.queue(
            name=retry_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": exchange_name,
                "x-dead-letter-routing-key": queue_name,
                "x-message-ttl": self._message_retry_ttl,
            },
        )
        dead_queue = await self._connection.queue(
            name=dead_letter_queue_name, durable=True
        )

        await queue.bind(exchange=exchange_name, routing_key=queue_name)
        await retry_queue.bind(exchange=retry_exchange_name, routing_key=queue_name)
        await dead_queue.bind(
            exchange=dead_letter_exchange_name,
            routing_key=queue_name,
        )

        for event_class in subscriber.subscribed_to():
            await queue.bind(
                exchange=exchange_name,
                routing_key=event_class.event_name(),
            )

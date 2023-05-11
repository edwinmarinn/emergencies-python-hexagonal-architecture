import asyncio
from typing import Iterable

from aio_pika import Message

from contexts.shared.domain.bus.event import (
    DomainEvent,
    DomainEventSubscriber,
    EventBus,
)
from contexts.shared.infrastructure.bus.event.domain_event_json_serializer import (
    DomainEventJsonSerializer,
)

from ...domain_event_json_deserializer import DomainEventJsonDeserializer
from ...domain_event_mapping import DomainEventMapping
from ..rabbit_mq_queue_name_formatter import RabbitMqQueueNameFormatter
from .rabbit_mq_connection_async import RabbitMqConnectionAsync
from .rabbit_mq_domain_events_consumer_async import RabbitMqDomainEventsConsumerAsync


class RabbitMqEventBusAsync(EventBus):
    def __init__(
        self,
        connection: RabbitMqConnectionAsync,
        exchange_name: str,
        queue_name_formatter: RabbitMqQueueNameFormatter,
        max_retries: int,
        # failover_publisher: MySqlEventBus
    ):
        self._connection = connection
        self._exchange_name = exchange_name
        self._queue_name_formatter = queue_name_formatter
        self._max_retries = max_retries

    async def publish(self, *events: DomainEvent) -> None:
        tasks = [asyncio.create_task(self._publisher(event)) for event in events]
        await asyncio.gather(*tasks)

    async def _publisher(self, event: DomainEvent):
        await self._publish_event(event)
        # try:
        #     await self._publish_event(event)
        # except Exception as e:
        #     pass

    async def _publish_event(self, event: DomainEvent) -> None:
        body = DomainEventJsonSerializer.serialize_bytes(event)
        routing_key = event.event_name()
        message_id = event.event_id

        exchange = await self._connection.exchange(self._exchange_name)
        await exchange.publish(
            message=Message(
                body=body,
                content_type="application/json",
                content_encoding="utf-8",
                message_id=message_id,
            ),
            routing_key=routing_key,
        )

    async def add_subscribers(
        self, subscribers: Iterable[DomainEventSubscriber]
    ) -> None:
        deserializer = DomainEventJsonDeserializer(
            domain_event_mapping=DomainEventMapping(subscribers)
        )

        for subscriber in subscribers:
            queue_name = self._queue_name_formatter.format(subscriber=subscriber)
            rabbit_mq_consumer = RabbitMqDomainEventsConsumerAsync(
                connection=self._connection,
                deserializer=deserializer,
                exchange_name=self._exchange_name,
                queue_name=queue_name,
                max_retries=self._max_retries,
            )
            await rabbit_mq_consumer.consume(subscriber=subscriber)

from aio_pika import Message

from contexts.shared.domain.bus.event import DomainEvent, EventBus
from contexts.shared.infrastructure.bus.event.domain_event_json_serializer import (
    DomainEventJsonSerializer,
)

from .rabbit_mq_connection_async import RabbitMqConnectionAsync


class RabbitMqEventBusAsync(EventBus):
    def __init__(
        self,
        connection: RabbitMqConnectionAsync,
        exchange_name: str,
        # failover_publisher: MySqlEventBus
    ):
        self._connection = connection
        self._exchange_name = exchange_name

    async def publish(self, *events: DomainEvent) -> None:
        for event in events:
            await self._publisher(event)

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

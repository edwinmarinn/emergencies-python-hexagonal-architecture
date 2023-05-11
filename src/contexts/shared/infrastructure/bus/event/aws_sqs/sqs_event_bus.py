import asyncio
from typing import Iterable

from contexts.shared.domain.bus.event import (
    DomainEvent,
    DomainEventSubscriber,
    EventBus,
)
from contexts.shared.infrastructure.bus.event import DomainEventJsonSerializer
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_connection import (
    SqsConnection,
    SqsConnectionManager,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_queue_name_formatter import (
    SqsQueueNameFormatter,
)


class SqsEventBus(EventBus):
    def __init__(
        self,
        connection_manager: SqsConnectionManager,
        sns_topic_name: str,
        queue_name_formatter: SqsQueueNameFormatter,
        max_retries: int,
    ):
        self._connection_manager = connection_manager
        self._sns_topic_name = sns_topic_name
        self._queue_name_formatter = queue_name_formatter
        self._max_retries = max_retries

    async def publish(self, *events: DomainEvent) -> None:
        async with self._connection_manager.connect() as connection:
            tasks = [
                asyncio.create_task(self._publisher(event, connection))
                for event in events
            ]
            await asyncio.gather(*tasks)

    async def _publisher(self, event: DomainEvent, connection: SqsConnection):
        await self._publish_event(event, connection)
        # try:
        #     await self._publish_event(event)
        # except Exception as e:
        #     pass

    async def _publish_event(
        self, event: DomainEvent, connection: SqsConnection
    ) -> None:
        body = DomainEventJsonSerializer.serialize(event)
        routing_key = event.event_name()
        message_id = event.event_id

        await connection.publish(
            topic_name=self._sns_topic_name, message=body, routing_key=routing_key
        )

    async def add_subscribers(self, subscribers: Iterable[DomainEventSubscriber]):
        pass

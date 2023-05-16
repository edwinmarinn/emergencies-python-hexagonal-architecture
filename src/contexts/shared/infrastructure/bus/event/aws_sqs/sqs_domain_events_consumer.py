from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_connection import (
    SqsConnection,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_queue import (
    SqsIncomingMessage,
)
from contexts.shared.infrastructure.bus.event.domain_event_json_deserializer import (
    DomainEventJsonDeserializer,
)


class SqsDomainEventsConsumer:
    def __init__(
        self,
        connection: SqsConnection,
        deserializer: DomainEventJsonDeserializer,
        topic_name: str,
        queue_name: str,
        retry_visibility_timeout: int,
        consume_interval: int,
    ):
        self._connection = connection
        self._deserializer = deserializer
        self._topic_name = topic_name
        self._queue_name = queue_name
        self._retry_visibility_timeout = retry_visibility_timeout
        self._consume_interval = consume_interval

    async def consume(self, subscriber) -> None:
        queue = await self._connection.queue(self._queue_name)
        await queue.consume(
            callback=self._consumer(subscriber), consume_interval=self._consume_interval
        )

    def _consumer(self, subscriber):
        async def wrapper(message: SqsIncomingMessage):
            event = self._deserializer.deserialize(message.body)

            try:
                await subscriber(event)
                await message.ack()
            except Exception:
                await self._handle_consumption_error(message)

        return wrapper

    async def _handle_consumption_error(self, message: SqsIncomingMessage) -> None:
        await message.noack(visibility_timeout=self._retry_visibility_timeout)

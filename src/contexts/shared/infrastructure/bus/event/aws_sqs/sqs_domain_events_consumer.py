from typing import cast

from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage

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
        max_retries: int,
    ):
        self._connection = connection
        self._deserializer = deserializer
        self._topic_name = topic_name
        self._queue_name = queue_name
        self._max_retries = max_retries

    async def consume(self, subscriber) -> None:
        queue = await self._connection.queue(self._queue_name)
        await queue.consume(self._consumer(subscriber))

    def _consumer(self, subscriber):
        async def wrapper(message: SqsIncomingMessage):
            event = self._deserializer.deserialize(message.body)

            try:
                await subscriber(event)
            except Exception as error:
                # await self._handle_consumption_error(message)
                raise error

            await message.ack()

        return wrapper

    # async def _handle_consumption_error(self, message: AbstractIncomingMessage) -> None:
    #     if self._has_been_redelivered_too_much(message):
    #         await self._send_to_dead_letter(message)
    #     else:
    #         await self._send_to_retry(message)
    #
    #     await message.ack()

    # def _has_been_redelivered_too_much(self, message: AbstractIncomingMessage) -> bool:
    #     return self._get_redelivery_count_header(message) >= self._max_retries

    # async def _send_to_dead_letter(self, message: AbstractIncomingMessage) -> None:
    #     await self._send_message_to(
    #         RabbitMqExchangeNameFormatter.dead_letter(self._topic_name), message
    #     )

    # async def _send_to_retry(self, message: AbstractIncomingMessage) -> None:
    #     await self._send_message_to(
    #         RabbitMqExchangeNameFormatter.retry(self._topic_name), message
    #     )

    # @staticmethod
    # def _get_redelivery_count_header(message: AbstractIncomingMessage) -> int:
    #     count = message.headers.get(_REDELIVERY_COUNT_HEADER, 0)
    #     return cast(int, count)

    # async def _send_message_to(
    #     self, exchange_name: str, message: AbstractIncomingMessage
    # ) -> None:
    #     headers = message.headers.copy()
    #     headers[_REDELIVERY_COUNT_HEADER] = (
    #         self._get_redelivery_count_header(message) + 1
    #     )
    #
    #     exchange = await self._connection.exchange(exchange_name)
    #
    #     await exchange.publish(
    #         message=Message(
    #             body=message.body,
    #             content_type=message.content_type,
    #             content_encoding=message.content_encoding,
    #             message_id=message.message_id,
    #             priority=message.priority,
    #             headers=headers,
    #         ),
    #         routing_key=self._queue_name,
    #     )

from typing import cast

from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage

from ...domain_event_json_deserializer import DomainEventJsonDeserializer
from ..rabbit_mq_exchange_name_formatter import RabbitMqExchangeNameFormatter
from .rabbit_mq_connection_async import RabbitMqConnectionAsync

_REDELIVERY_COUNT_HEADER = "redelivery_count"


class RabbitMqDomainEventsConsumerAsync:
    def __init__(
        self,
        connection: RabbitMqConnectionAsync,
        deserializer: DomainEventJsonDeserializer,
        exchange_name: str,
        queue_name: str,
        max_retries: int,
    ):
        self._connection = connection
        self._deserializer = deserializer
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._max_retries = max_retries

    async def consume(self, subscriber) -> None:
        queue = await self._connection.queue(self._queue_name)
        await queue.consume(self._consumer(subscriber))

    def _consumer(self, subscriber):
        async def wrapper(message: AbstractIncomingMessage):
            event = self._deserializer.deserialize(message.body)

            try:
                await subscriber(event)
            except Exception:
                await self._handle_consumption_error(message)
            finally:
                await message.ack()

        return wrapper

    async def _handle_consumption_error(self, message: AbstractIncomingMessage) -> None:
        if self._has_been_redelivered_too_much(message):
            await self._send_to_dead_letter(message)
        else:
            await self._send_to_retry(message)

    def _has_been_redelivered_too_much(self, message: AbstractIncomingMessage) -> bool:
        return self._get_redelivery_count_header(message) >= self._max_retries

    async def _send_to_dead_letter(self, message: AbstractIncomingMessage) -> None:
        await self._send_message_to(
            RabbitMqExchangeNameFormatter.dead_letter(self._exchange_name), message
        )

    async def _send_to_retry(self, message: AbstractIncomingMessage) -> None:
        await self._send_message_to(
            RabbitMqExchangeNameFormatter.retry(self._exchange_name), message
        )

    @staticmethod
    def _get_redelivery_count_header(message: AbstractIncomingMessage) -> int:
        count = message.headers.get(_REDELIVERY_COUNT_HEADER, 0)
        return cast(int, count)

    async def _send_message_to(
        self, exchange_name: str, message: AbstractIncomingMessage
    ) -> None:
        headers = message.headers.copy()
        headers[_REDELIVERY_COUNT_HEADER] = (
            self._get_redelivery_count_header(message) + 1
        )

        exchange = await self._connection.exchange(exchange_name)

        await exchange.publish(
            message=Message(
                body=message.body,
                content_type=message.content_type,
                content_encoding=message.content_encoding,
                message_id=message.message_id,
                priority=message.priority,
                headers=headers,
            ),
            routing_key=self._queue_name,
        )

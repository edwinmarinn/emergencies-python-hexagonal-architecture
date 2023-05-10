from typing import Iterable

from contexts.shared.domain.bus.event import DomainEventSubscriber
from contexts.shared.infrastructure.bus.event.aws_sqs.sns_topic_name_formatter import (
    SnsTopicNameFormatter,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_connection import (
    SqsConnection,
    SqsConnectionManager,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_queue_name_formatter import (
    SqsQueueNameFormatter,
)


class SqsConfigure:
    def __init__(
        self,
        connection_manager: SqsConnectionManager,
        queue_name_formatter: SqsQueueNameFormatter,
    ):
        self._connection_manager = connection_manager
        self._queue_name_formatter = queue_name_formatter

    async def configure(
        self, sns_topic_name: str, subscribers: Iterable[DomainEventSubscriber]
    ) -> None:
        async with self._connection_manager.connect() as connection:
            await self._declare_sns_topics(sns_topic_name, connection=connection)
            await self._declare_queues_for_subscribers(
                subscribers, sns_topic_name, connection=connection
            )

    async def _declare_sns_topics(
        self, sns_topic_name: str, connection: SqsConnection
    ) -> None:
        retry_sns_topic_name = SnsTopicNameFormatter.retry(sns_topic_name)
        dead_letter_sns_topic_name = SnsTopicNameFormatter.dead_letter(sns_topic_name)

        names = (sns_topic_name, retry_sns_topic_name, dead_letter_sns_topic_name)

        for name in names:
            response = await connection.create_topic(name=name)

    async def _declare_queues_for_subscribers(
        self,
        subscribers: Iterable[DomainEventSubscriber],
        exchange_name: str,
        connection: SqsConnection,
    ):
        retry_exchange_name = SnsTopicNameFormatter.retry(exchange_name)
        dead_letter_exchange_name = SnsTopicNameFormatter.dead_letter(exchange_name)

        for subscriber in subscribers:
            await self._queue_declarator(
                subscriber,
                exchange_name=exchange_name,
                retry_exchange_name=retry_exchange_name,
                dead_letter_exchange_name=dead_letter_exchange_name,
                connection=connection,
            )

    async def _queue_declarator(
        self,
        subscriber: DomainEventSubscriber,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
        connection: SqsConnection,
    ) -> None:
        queue_name = self._queue_name_formatter.format(subscriber)
        retry_queue_name = self._queue_name_formatter.format_retry(subscriber)
        dead_letter_queue_name = self._queue_name_formatter.format_dead_letter(
            subscriber
        )

        # Declare queues
        queue = await connection.create_queue(name=queue_name)
        retry_queue = await connection.create_queue(name=retry_queue_name)
        dead_letter_queue = await connection.create_queue(name=dead_letter_queue_name)

        # Bind queue
        await connection.queue_bind(
            queue_name=queue_name,
            topic_name=exchange_name,
            routing_keys=[queue_name, *self.get_routing_keys(subscriber)],
        )
        await connection.queue_bind(
            queue_name=retry_queue_name,
            topic_name=retry_exchange_name,
            routing_keys=[queue_name],
        )
        await connection.queue_bind(
            queue_name=dead_letter_queue_name,
            topic_name=dead_letter_exchange_name,
            routing_keys=[queue_name],
        )

    @staticmethod
    def get_routing_keys(subscriber: DomainEventSubscriber):
        return [event_class.event_name() for event_class in subscriber.subscribed_to()]

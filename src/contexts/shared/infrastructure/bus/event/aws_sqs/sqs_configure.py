import asyncio
from typing import Iterable

from contexts.shared.domain.bus.event import DomainEventSubscriber
from contexts.shared.infrastructure.bus.event.aws_sqs.sns_topic_name_formatter import (
    SnsTopicNameFormatter,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_connection import (
    SqsConnection,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_queue_name_formatter import (
    SqsQueueNameFormatter,
)


class SqsConfigurer:
    def __init__(
        self,
        connection: SqsConnection,
        queue_name_formatter: SqsQueueNameFormatter,
    ):
        self._connection = connection
        self._queue_name_formatter = queue_name_formatter

    async def configure(
        self, sns_topic_name: str, subscribers: Iterable[DomainEventSubscriber]
    ) -> None:
        await self._declare_sns_topics(sns_topic_name)
        await self._declare_queues_for_subscribers(subscribers, sns_topic_name)

    async def _declare_sns_topics(self, sns_topic_name: str) -> None:
        retry_sns_topic_name = SnsTopicNameFormatter.retry(sns_topic_name)
        dead_letter_sns_topic_name = SnsTopicNameFormatter.dead_letter(sns_topic_name)

        names = (sns_topic_name, retry_sns_topic_name, dead_letter_sns_topic_name)

        tasks = [self._connection.topic(name=name) for name in names]
        await asyncio.gather(*tasks)

    async def _declare_queues_for_subscribers(
        self, subscribers: Iterable[DomainEventSubscriber], exchange_name: str
    ):
        retry_exchange_name = SnsTopicNameFormatter.retry(exchange_name)
        dead_letter_exchange_name = SnsTopicNameFormatter.dead_letter(exchange_name)

        tasks = [
            self._queue_declarator(
                subscriber,
                exchange_name=exchange_name,
                retry_exchange_name=retry_exchange_name,
                dead_letter_exchange_name=dead_letter_exchange_name,
            )
            for subscriber in subscribers
        ]
        await asyncio.gather(*tasks)

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
        await asyncio.gather(
            self._connection.queue(name=queue_name),
            self._connection.queue(name=retry_queue_name),
            self._connection.queue(name=dead_letter_queue_name),
        )

        # Bind queue
        await asyncio.gather(
            self._connection.queue_bind(
                queue_name=queue_name,
                topic_name=exchange_name,
                routing_keys=[queue_name, *self.get_routing_keys(subscriber)],
            ),
            self._connection.queue_bind(
                queue_name=retry_queue_name,
                topic_name=retry_exchange_name,
                routing_keys=[queue_name],
            ),
            self._connection.queue_bind(
                queue_name=dead_letter_queue_name,
                topic_name=dead_letter_exchange_name,
                routing_keys=[queue_name],
            ),
        )

    @staticmethod
    def get_routing_keys(subscriber: DomainEventSubscriber):
        return [event_class.event_name() for event_class in subscriber.subscribed_to()]

import asyncio
import json
from typing import Iterable

from contexts.shared.domain.bus.event import DomainEventSubscriber
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
        max_receive_count: int,
    ):
        self._connection = connection
        self._queue_name_formatter = queue_name_formatter
        self._max_receive_count = max_receive_count

    async def configure(
        self, sns_topic_name: str, subscribers: Iterable[DomainEventSubscriber]
    ) -> None:
        await self._declare_sns_topics(sns_topic_name)
        await self._declare_queues_for_subscribers(subscribers, sns_topic_name)

    async def _declare_sns_topics(self, sns_topic_name: str) -> None:
        await self._connection.topic(name=sns_topic_name)

    async def _declare_queues_for_subscribers(
        self, subscribers: Iterable[DomainEventSubscriber], topic_name: str
    ):
        tasks = [
            self._queue_declarator(
                subscriber,
                topic_name=topic_name,
            )
            for subscriber in subscribers
        ]
        await asyncio.gather(*tasks)

    async def _queue_declarator(
        self,
        subscriber: DomainEventSubscriber,
        topic_name: str,
    ) -> None:
        queue_name = self._queue_name_formatter.format(subscriber)
        dead_letter_queue_name = self._queue_name_formatter.format_dead_letter(
            subscriber
        )

        dead_letter_queue = await self._connection.queue(name=dead_letter_queue_name)
        queue = await self._connection.queue(
            name=queue_name,
            attributes={
                "RedrivePolicy": json.dumps(
                    {
                        "deadLetterTargetArn": dead_letter_queue.arn,
                        "maxReceiveCount": self._max_receive_count,
                    }
                )
            },
        )

        # Bind queue
        await self._connection.queue_bind(
            queue=queue,
            topic_name=topic_name,
            routing_keys=[queue_name, *self.get_routing_keys(subscriber)],
        )

    @staticmethod
    def get_routing_keys(subscriber: DomainEventSubscriber):
        return [event_class.event_name() for event_class in subscriber.subscribed_to()]

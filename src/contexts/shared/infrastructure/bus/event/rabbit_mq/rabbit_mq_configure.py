from typing import Iterable

from pika.exchange_type import ExchangeType

from contexts.shared.domain.bus.event import DomainEventSubscriber

from .rabbit_mq_connection import RabbitMqConnection
from .rabbit_mq_exchange_name_formatter import RabbitMqExchangeNameFormatter
from .rabbit_mq_queue_name_formatter import RabbitMqQueueNameFormatter


class RabbitMqConfigurer:
    def __init__(self, connection: RabbitMqConnection, message_retry_ttl=100) -> None:
        self._connection = connection
        self._message_retry_ttl = message_retry_ttl

    def configure(
        self, exchange_name: str, subscribers: Iterable[DomainEventSubscriber]
    ) -> None:
        retry_exchange_name = RabbitMqExchangeNameFormatter.retry(exchange_name)
        dead_letter_exchange_name = RabbitMqExchangeNameFormatter.dead_letter(
            exchange_name
        )

        self._exchange_declare(exchange_name)
        self._exchange_declare(retry_exchange_name)
        self._exchange_declare(dead_letter_exchange_name)

        for subscriber in subscribers:
            self._queue_declarator(
                subscriber,
                exchange_name=exchange_name,
                retry_exchange_name=retry_exchange_name,
                dead_letter_exchange_name=dead_letter_exchange_name,
            )

    def _exchange_declare(self, exchange_name: str) -> None:
        self._connection.exchange_declare(
            exchange_name=exchange_name, exchange_type=ExchangeType.topic, durable=True
        )

    def _queue_declarator(
        self,
        subscriber: DomainEventSubscriber,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
    ) -> None:
        queue_name = RabbitMqQueueNameFormatter.format(subscriber)
        retry_queue_name = RabbitMqQueueNameFormatter.format_retry(subscriber)
        dead_letter_queue_name = RabbitMqQueueNameFormatter.format_dead_letter(
            subscriber
        )

        # Declare queues
        self._connection.queue_declare(name=queue_name, durable=True)
        self._connection.queue_declare(
            name=retry_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": exchange_name,
                "x-dead-letter-routing-key": queue_name,
                "x-message-ttl": self._message_retry_ttl,
            },
        )
        self._connection.queue_declare(name=dead_letter_queue_name, durable=True)

        self._connection.channel().queue_bind(
            queue=queue_name, exchange=exchange_name, routing_key=queue_name
        )
        self._connection.channel().queue_bind(
            queue=retry_queue_name, exchange=retry_exchange_name, routing_key=queue_name
        )
        self._connection.channel().queue_bind(
            queue=dead_letter_queue_name,
            exchange=dead_letter_exchange_name,
            routing_key=queue_name,
        )

        for event_class in subscriber.subscribed_to():
            self._connection.channel().queue_bind(
                queue=queue_name,
                exchange=exchange_name,
                routing_key=event_class.event_name(),
            )

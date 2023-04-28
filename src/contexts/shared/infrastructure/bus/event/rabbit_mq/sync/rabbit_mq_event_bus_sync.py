from contexts.shared.domain.bus.event import DomainEvent, EventBus
from contexts.shared.infrastructure.bus.event.domain_event_json_serializer import (
    DomainEventJsonSerializer,
)

from .rabbit_mq_connection_sync import RabbitMqConnectionSync


class RabbitMqEventBusSync(EventBus):
    def __init__(
        self,
        connection: RabbitMqConnectionSync,
        exchange_name: str,
        # failover_publisher: MySqlEventBus
    ):
        self._connection = connection
        self._exchange_name = exchange_name

    async def publish(self, *events: DomainEvent) -> None:
        for event in events:
            self._publisher(event)

    def _publisher(self, event: DomainEvent):
        try:
            self._publish_event(event)
        except Exception:
            pass
        # except(AMQPException):
        #     $this->failoverPublisher->publish($event);

    def _publish_event(self, event: DomainEvent) -> None:
        body = DomainEventJsonSerializer.serialize(event)
        routing_key = event.event_name()
        message_id = event.event_id

        self._connection.channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=routing_key,
            body=body,
            # properties={
            #     'message_id': message_id,
            #     'content_type': 'application/json',
            #     'content_encoding': 'utf-8',
            # }
        )

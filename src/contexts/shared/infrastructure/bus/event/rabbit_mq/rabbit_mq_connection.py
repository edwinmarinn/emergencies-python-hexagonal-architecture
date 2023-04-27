from typing import Any, Dict, TypedDict

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType


class ConnectionSettings(TypedDict):
    url: str


class RabbitMqConnection:
    _connection: pika.BlockingConnection | None = None
    _channel: BlockingChannel | None = None
    _exchanges: Dict[str, Any] = {}
    _queues: Dict[str, Any] = {}

    def __init__(self, connection_settings: ConnectionSettings):
        self.connection_settings = connection_settings

    def queue_declare(self, name, durable=True, arguments: dict | None = None) -> None:
        if name not in self._queues:
            queue_ok = self.channel().queue_declare(
                queue=name, durable=durable, arguments=arguments
            )
            self._queues[name] = queue_ok

    def exchange_declare(
        self,
        exchange_name: str,
        exchange_type: ExchangeType = ExchangeType.topic,
        durable: bool = True,
    ) -> None:
        if exchange_name not in self._exchanges:
            exchange_ok = self.channel().exchange_declare(
                exchange=exchange_name,
                exchange_type=exchange_type,  # Type: ignore
                durable=durable,
            )
            self._exchanges[exchange_name] = exchange_ok

    def channel(self) -> BlockingChannel:
        if not self._channel or self._channel.is_closed:
            self._channel = self.connection().channel()

        return self._channel

    def connection(self) -> pika.BlockingConnection:
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(
                pika.URLParameters(self.connection_settings["url"])
            )
        return self._connection

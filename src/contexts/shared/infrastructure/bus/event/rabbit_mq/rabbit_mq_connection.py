from typing import Any, Dict, TypedDict

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType


class RabbitMqConnectionSettings(TypedDict):
    host: str
    port: int
    virtual_host: str
    username: str
    password: str


class RabbitMqConnection:
    def __init__(self, connection_settings: RabbitMqConnectionSettings):
        self._connection_settings = connection_settings

        self._connection: pika.BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    @property
    def channel(self) -> BlockingChannel:
        if not self._channel or self._channel.is_closed:
            self._channel = self.connection.channel()

        return self._channel

    @property
    def connection(self) -> pika.BlockingConnection:
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._connection_settings["host"],
                    port=self._connection_settings["port"],
                    virtual_host=self._connection_settings["virtual_host"],
                    credentials=pika.PlainCredentials(
                        username=self._connection_settings["username"],
                        password=self._connection_settings["password"],
                    ),
                )
            )
        return self._connection

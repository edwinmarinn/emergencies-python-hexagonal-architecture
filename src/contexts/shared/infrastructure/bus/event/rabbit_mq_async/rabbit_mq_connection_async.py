from typing import Dict, TypedDict, cast

import aio_pika
import pamqp.common
from aio_pika import (
    ExchangeType,
    RobustChannel,
    RobustConnection,
)
from aio_pika.abc import AbstractRobustExchange
from aio_pika.abc import AbstractRobustQueue


class RabbitMqConnectionSettings(TypedDict):
    host: str
    port: int
    virtual_host: str
    username: str
    password: str


class RabbitMqConnectionAsync:
    def __init__(self, connection_settings: RabbitMqConnectionSettings):
        self._connection_settings = connection_settings

        self._connection: RobustConnection | None = None
        self._channel: RobustChannel | None = None
        self._exchanges: Dict[str, AbstractRobustExchange ] = {}
        self._queues: Dict[str, AbstractRobustQueue] = {}

    async def exchange(
        self, name: str, type: ExchangeType = ExchangeType.TOPIC, durable: bool = True
    ) -> AbstractRobustExchange:
        if name not in self._exchanges:
            channel = await self.channel
            self._exchanges[name] = await channel.declare_exchange(
                name=name, type=type, durable=durable
            )

        return self._exchanges[name]

    async def queue(
        self,
        name: str,
        durable: bool = True,
        arguments: pamqp.common.Arguments | None = None,
    ) -> AbstractRobustQueue:
        if name not in self._queues:
            channel = await self.channel
            self._queues[name] = await channel.declare_queue(
                name=name, durable=durable, arguments=arguments
            )

        return self._queues[name]

    @property
    async def channel(self) -> RobustChannel:
        if not self._channel or self._channel.is_closed:
            connection = await self.connection
            channel = await connection.channel()
            self._channel = cast(RobustChannel, channel)

        return self._channel

    @property
    async def connection(self) -> RobustConnection:
        if not self._connection or self._connection.is_closed:
            connection = await aio_pika.connect_robust(
                host=self._connection_settings["host"],
                port=self._connection_settings["port"],
                login=self._connection_settings["username"],
                password=self._connection_settings["password"],
                virtualhost=self._connection_settings["virtual_host"],
                connection_class=RobustConnection,
            )
            self._connection = cast(RobustConnection, connection)

        return self._connection

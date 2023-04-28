from typing import TypedDict


class RabbitMqConnectionSettings(TypedDict):
    host: str
    port: int
    virtual_host: str
    username: str
    password: str

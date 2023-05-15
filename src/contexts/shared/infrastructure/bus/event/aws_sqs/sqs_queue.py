import asyncio
import json
from asyncio import Task
from typing import Any, Awaitable, Callable, Dict

from typing_extensions import Self


class SqsIncomingMessage:
    def __init__(self, message, queue: "SqsQueue"):
        self._message_id = message["MessageId"]
        self._receipt_handle = message["ReceiptHandle"]
        self._med5_of_body = message["MD5OfBody"]

        general_body = json.loads(message["Body"])
        self._body = general_body["Message"]

        self._queue = queue
        self._sqs_client = self._queue.sqs_client

    @property
    def body(self):
        return self._body

    async def ack(self):
        # Delete the message from the queue
        await self._sqs_client.delete_message(
            QueueUrl=self._queue.url, ReceiptHandle=self._receipt_handle
        )


MessageCallable = Callable[[SqsIncomingMessage], Awaitable[Any]]


class SqsQueue:
    def __init__(self, queue_response, sqs_client):
        self._url: str = queue_response["QueueUrl"]
        self._arn: str = ""
        self._attributes: Dict[str, str] = {}

        self._sqs_client = sqs_client

        # Important to maintain task references and prevent them from being collected by the garbage collector
        self._consume_tasks: Dict[MessageCallable, Task] = {}

    async def _init(self):
        response = await self._sqs_client.get_queue_attributes(
            QueueUrl=self._url, AttributeNames=["QueueArn"]
        )
        self._attributes = response["Attributes"]

    @classmethod
    async def create(cls, queue_response, sqs_client) -> Self:
        obj = cls(queue_response, sqs_client)
        await obj._init()
        return obj

    @property
    def sqs_client(self):
        return self._sqs_client

    @property
    def url(self) -> str:
        return self._url

    @property
    def arn(self) -> str:
        return self._attributes["QueueArn"]

    async def __consume_coroutine(self, callback: MessageCallable):
        while True:
            response = await self._sqs_client.receive_message(
                QueueUrl=self.url, MaxNumberOfMessages=10, WaitTimeSeconds=20
            )
            if "Messages" in response:
                for _message in response["Messages"]:
                    sqs_message = SqsIncomingMessage(message=_message, queue=self)
                    await callback(sqs_message)
            else:
                await asyncio.sleep(10)

    async def consume(self, callback: MessageCallable):
        if callback not in self._consume_tasks:
            task = asyncio.create_task(self.__consume_coroutine(callback))
            self._consume_tasks[callback] = task

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
        await self._sqs_client.delete_message(
            QueueUrl=self._queue.url, ReceiptHandle=self._receipt_handle
        )

    async def noack(self, visibility_timeout: int = 30):
        await self._sqs_client.change_message_visibility(
            QueueUrl=self._queue.url,
            ReceiptHandle=self._receipt_handle,
            VisibilityTimeout=visibility_timeout,
        )


MessageCallable = Callable[[SqsIncomingMessage], Awaitable[Any]]


class SqsQueue:
    def __init__(self, queue_response: Dict[str, str], sqs_client):
        self._queue_response = queue_response
        self._attributes: Dict[str, str] = {}

        self._sqs_client = sqs_client

        # Important to maintain task references and prevent them from being collected by the garbage collector
        self._consume_tasks: Dict[MessageCallable, Task] = {}

    async def _init(self):
        response = await self._sqs_client.get_queue_attributes(
            QueueUrl=self.url, AttributeNames=["QueueArn"]
        )
        self._attributes = response["Attributes"]

    @classmethod
    async def create(cls, queue_response, sqs_client) -> Self:
        obj = cls(queue_response=queue_response, sqs_client=sqs_client)
        await obj._init()
        return obj

    @property
    def sqs_client(self):
        return self._sqs_client

    @property
    def url(self) -> str:
        return self._queue_response["QueueUrl"]

    @property
    def arn(self) -> str:
        return self._attributes["QueueArn"]

    async def __consume_coroutine(
        self, callback: MessageCallable, consume_interval: int
    ):
        while True:
            response = await self._sqs_client.receive_message(
                QueueUrl=self.url, MaxNumberOfMessages=10, WaitTimeSeconds=20
            )
            if "Messages" in response:
                for _message in response["Messages"]:
                    sqs_message = SqsIncomingMessage(message=_message, queue=self)
                    try:
                        await callback(sqs_message)
                    except Exception as e:
                        # This is executed in background as a task, so we need to avoid exit the task
                        # TODO: include logging to have the history of errors
                        pass
            else:
                await asyncio.sleep(consume_interval)

    async def consume(self, callback: MessageCallable, consume_interval: int):
        if callback not in self._consume_tasks:
            task = asyncio.create_task(
                self.__consume_coroutine(
                    callback=callback, consume_interval=consume_interval
                )
            )
            self._consume_tasks[callback] = task

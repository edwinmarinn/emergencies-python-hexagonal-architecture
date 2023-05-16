import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_queue import SqsQueue


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

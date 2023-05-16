import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List

from aiobotocore.session import AioSession
from typing_extensions import Self

from contexts.shared.infrastructure.bus.event.aws_sqs.sns_topic import SnsTopic
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_connection_settings import (
    SqsConnectionSettings,
)
from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_queue import SqsQueue


class SqsConnection:
    def __init__(self, connection_settings: SqsConnectionSettings):
        self._connection_settings = connection_settings

        self._exit_stack = AsyncExitStack()
        self._session: AioSession = AioSession()
        self._sns_client: Any = None
        self._sqs_client: Any = None

        self._topics: Dict[str, SnsTopic] = {}
        self._queues: Dict[str, SqsQueue] = {}

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        await self.__aexit__(None, None, None)

    @property
    async def sns_client(self):
        if self._sns_client is None:
            self._sns_client = await self._exit_stack.enter_async_context(
                self._create_client("sns")
            )
        return self._sns_client

    @property
    async def sqs_client(self):
        if self._sqs_client is None:
            self._sqs_client = await self._exit_stack.enter_async_context(
                self._create_client("sqs")
            )
        return self._sqs_client

    def _create_client(self, service_name):
        return self._session.create_client(
            service_name,
            region_name=self._connection_settings["region"],
            aws_access_key_id=self._connection_settings["aws_access_key_id"],
            aws_secret_access_key=self._connection_settings["aws_secret_access_key"],
        )

    async def topic(self, name: str):
        if name not in self._topics:
            sns_client = await self.sns_client
            topic_response = await sns_client.create_topic(Name=name)
            self._topics[name] = await SnsTopic.create(
                topic_response=topic_response, sns_client=sns_client
            )
        return self._topics[name]

    async def queue(self, name: str, attributes: Any = None) -> SqsQueue:
        if name not in self._queues:
            sqs_client = await self.sqs_client
            attributes = attributes or {}

            queue_response = await sqs_client.create_queue(
                QueueName=name, Attributes=attributes
            )
            self._queues[name] = await SqsQueue.create(
                queue_response=queue_response, sqs_client=sqs_client
            )
        return self._queues[name]

    async def publish(self, topic_name: str, message: str, routing_key: str):
        sns_client = await self.sns_client
        topic = await self.topic(name=topic_name)

        await sns_client.publish(
            TopicArn=topic.arn,
            Message=message,
            MessageAttributes={
                "event_type": {"DataType": "String", "StringValue": routing_key}
            },
        )

    async def queue_bind(
        self, queue: SqsQueue, topic_name: str, routing_keys: List[str]
    ):
        topic = await self.topic(name=topic_name)

        await self._allow_topic_publish_to_queue(
            topic=topic,
            queue=queue,
        )

        sns_client = await self.sns_client

        supscription = await sns_client.subscribe(
            TopicArn=topic.arn,
            Protocol="sqs",
            Endpoint=queue.arn,
        )

        await sns_client.set_subscription_attributes(
            SubscriptionArn=supscription["SubscriptionArn"],
            AttributeName="FilterPolicy",
            AttributeValue=json.dumps({"event_type": routing_keys}),
        )

    async def _allow_topic_publish_to_queue(self, topic: SnsTopic, queue: SqsQueue):
        sqs_client = await self.sqs_client

        access_policy = json.dumps(
            {
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "sns.amazonaws.com"},
                        "Action": "sqs:SendMessage",
                        "Resource": queue.arn,
                        "Condition": {"ArnEquals": {"aws:SourceArn": topic.arn}},
                    }
                ]
            }
        )

        response = await sqs_client.set_queue_attributes(
            QueueUrl=queue.url, Attributes={"Policy": access_policy}
        )

import json
from contextlib import AsyncExitStack
from typing import Any, List

from aiobotocore.session import AioSession
from typing_extensions import Self

from contexts.shared.infrastructure.bus.event.aws_sqs.sqs_connection_settings import (
    SqsConnectionSettings,
)


class SqsConnection:
    def __init__(self, connection_settings: SqsConnectionSettings):
        self._connection_settings = connection_settings

        self._exit_stack = AsyncExitStack()
        self._session: AioSession = AioSession()
        self._sns_client: Any = None
        self._sqs_client: Any = None

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

    async def create_topic(self, name: str):
        sns_client = await self.sns_client
        return await sns_client.create_topic(Name=name)

    async def create_queue(self, name: str):
        sqs_client = await self.sqs_client
        return await sqs_client.create_queue(QueueName=name)

    async def publish(self, topic_name: str, message: str, routing_key: str):
        sns_client = await self.sns_client
        await sns_client.publish(
            TopicArn=self.get_sns_arn(topic_name),
            Message=message,
            MessageAttributes={
                "event_type": {"DataType": "String", "StringValue": routing_key}
            },
        )

    async def queue_bind(self, queue_name, topic_name, routing_keys: List[str]):
        await self._allow_topic_publish_to_queue(
            topic_name=topic_name,
            queue_name=queue_name,
        )

        sns_client = await self.sns_client

        supscription = await sns_client.subscribe(
            TopicArn=self.get_sns_arn(topic_name),
            Protocol="sqs",
            Endpoint=self.get_sqs_arn(queue_name),
        )

        await sns_client.set_subscription_attributes(
            SubscriptionArn=supscription["SubscriptionArn"],
            AttributeName="FilterPolicy",
            AttributeValue=json.dumps({"event_type": routing_keys}),
        )

    async def _allow_topic_publish_to_queue(self, topic_name: str, queue_name: str):
        sns_arn = self.get_sns_arn(topic_name)
        sqs_arn = self.get_sqs_arn(queue_name)
        sqs_url = self.get_sqs_url(queue_name)

        sqs_client = await self.sqs_client

        access_policy = json.dumps(
            {
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "sns.amazonaws.com"},
                        "Action": "sqs:SendMessage",
                        "Resource": sqs_arn,
                        "Condition": {"ArnEquals": {"aws:SourceArn": sns_arn}},
                    }
                ]
            }
        )

        response = await sqs_client.set_queue_attributes(
            QueueUrl=sqs_url, Attributes={"Policy": access_policy}
        )

    def get_sqs_arn(self, queue_name: str) -> str:
        region = self._connection_settings["region"]
        account_id = self._connection_settings["account_id"]
        return f"arn:aws:sqs:{region}:{account_id}:{queue_name}"

    def get_sqs_url(self, queue_name: str) -> str:
        region = self._connection_settings["region"]
        account_id = self._connection_settings["account_id"]
        return f"https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}"

    def get_sns_arn(self, topic_name: str) -> str:
        region = self._connection_settings["region"]
        account_id = self._connection_settings["account_id"]
        return f"arn:aws:sns:{region}:{account_id}:{topic_name}"

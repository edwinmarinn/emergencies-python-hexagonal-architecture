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
        self._sqs_client = await self._exit_stack.enter_async_context(
            self._create_client("sqs")
        )
        self._sns_client = await self._exit_stack.enter_async_context(
            self._create_client("sns")
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    def _create_client(self, service_name):
        return self._session.create_client(
            service_name,
            region_name=self._connection_settings["region"],
            aws_access_key_id=self._connection_settings["aws_access_key_id"],
            aws_secret_access_key=self._connection_settings["aws_secret_access_key"],
        )

    async def create_topic(self, name: str):
        return await self._sns_client.create_topic(Name=name)

    async def create_queue(self, name: str):
        return await self._sqs_client.create_queue(QueueName=name)

    async def publish(self, topic_name: str, message: str, routing_key: str):
        await self._sns_client.publish(
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

        supscription = await self._sns_client.subscribe(
            TopicArn=self.get_sns_arn(topic_name),
            Protocol="sqs",
            Endpoint=self.get_sqs_arn(queue_name),
        )

        await self._sns_client.set_subscription_attributes(
            SubscriptionArn=supscription["SubscriptionArn"],
            AttributeName="FilterPolicy",
            AttributeValue=json.dumps({"event_type": routing_keys}),
        )

    async def _allow_topic_publish_to_queue(self, topic_name: str, queue_name: str):
        sns_arn = self.get_sns_arn(topic_name)
        sqs_arn = self.get_sqs_arn(queue_name)
        sqs_url = self.get_sqs_url(queue_name)

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

        response = await self._sqs_client.set_queue_attributes(
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


class SqsConnectionContext:
    def __init__(self, connection_settings: SqsConnectionSettings):
        self._connection_settings = connection_settings
        self._connection: SqsConnection | None = None

    async def __aenter__(self) -> SqsConnection:
        self._connection = SqsConnection(connection_settings=self._connection_settings)
        return await self._connection.__aenter__()

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if self._connection is not None:
            await self._connection.__aexit__(exc_type, exc_value, exc_tb)


class SqsConnectionManager:
    def __init__(self, connection_settings: SqsConnectionSettings):
        self._connection_settings = connection_settings

    def connect(self) -> SqsConnectionContext:
        return SqsConnectionContext(self._connection_settings)

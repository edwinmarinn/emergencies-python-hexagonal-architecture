from typing import Mapping

from typing_extensions import Self


class SnsTopic:
    def __init__(self, topic_response: Mapping[str, str], sns_client):
        self._topic_response = topic_response
        self._sns_client = sns_client

    async def _init(self):
        pass

    @classmethod
    async def create(cls, topic_response, sns_client) -> Self:
        obj = cls(topic_response=topic_response, sns_client=sns_client)
        await obj._init()
        return obj

    @property
    def arn(self) -> str:
        return self._topic_response["TopicArn"]

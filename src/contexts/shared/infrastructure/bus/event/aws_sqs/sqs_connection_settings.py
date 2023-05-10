from typing import TypedDict


class SqsConnectionSettings(TypedDict):
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    account_id: int

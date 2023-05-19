from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDbDatabaseConnection:
    def __init__(self, client: AsyncIOMotorClient, database_name: str):
        self._client = client
        self._database: AsyncIOMotorDatabase = self._client[database_name]

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self._database

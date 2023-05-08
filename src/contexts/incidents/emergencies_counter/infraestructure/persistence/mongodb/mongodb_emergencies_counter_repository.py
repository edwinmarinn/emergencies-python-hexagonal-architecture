import asyncio

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from contexts.incidents.emergencies_counter.domain.entities import (
    EmergenciesCounter,
    EmergenciesCounterRepository,
)


class MongodbEmergenciesCounterRepository(EmergenciesCounterRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._db: AsyncIOMotorDatabase = self._client["incidents"]
        self._collection: AsyncIOMotorCollection = self._db["emergencies_counter"]

    async def save(self, counter: EmergenciesCounter) -> None:
        data = counter.to_primitives()
        _filter = {"_id": data.pop("id")}
        update = {"$set": data}
        await asyncio.sleep(15)  # To demonstrate possible race conditions
        await self._collection.update_one(filter=_filter, update=update, upsert=True)

    async def search(self) -> EmergenciesCounter | None:
        data = await self._collection.find_one()

        if not data:
            return None

        emergencies_counter = EmergenciesCounter.from_primitives(data)
        return emergencies_counter

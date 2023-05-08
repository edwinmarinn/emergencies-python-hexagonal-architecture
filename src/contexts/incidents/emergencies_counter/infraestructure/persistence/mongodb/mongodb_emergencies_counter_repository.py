from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo import ReturnDocument

from contexts.incidents.emergencies_counter.domain.entities import (
    EmergenciesCounter,
    EmergenciesCounterRepository,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId


class MongodbEmergenciesCounterRepository(EmergenciesCounterRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._db: AsyncIOMotorDatabase = self._client["incidents"]
        self._collection_counter: AsyncIOMotorCollection = self._db[
            "emergencies_counter"
        ]
        self._collection_counter_map: AsyncIOMotorCollection = self._db[
            "emergencies_counter_map"
        ]

    async def has_incremented(self, emergency_id: EmergencyId) -> bool:
        document = await self._collection_counter_map.find_one(
            filter={"_id": emergency_id.value}
        )
        return document is not None

    async def increment(
        self, counter: EmergenciesCounter, emergency_id: EmergencyId
    ) -> EmergenciesCounter:
        await self._collection_counter_map.insert_one(
            document={"_id": emergency_id.value}
        )

        document = await self._collection_counter.find_one_and_update(
            filter={"_id": counter.id.value},
            update={"$inc": {"total": 1}},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )

        emergencies_counter = EmergenciesCounter.from_primitives(document)
        return emergencies_counter

    async def search(self) -> EmergenciesCounter | None:
        data = await self._collection_counter.find_one()

        if not data:
            return None

        emergencies_counter = EmergenciesCounter.from_primitives(data)
        return emergencies_counter

from pymongo import ReturnDocument

from contexts.incidents.emergencies_counter_per_user.domain.entities import (
    EmergenciesCounterPerUser,
    EmergenciesCounterPerUserRepository,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.infrastructure.persistence.mongodb import MongoDbDatabaseConnection


class MongodbEmergenciesCounterPerUserRepository(EmergenciesCounterPerUserRepository):
    def __init__(self, connection: MongoDbDatabaseConnection):
        self._collection_counter = connection.database["emergencies_counter_per_user"]
        self._collection_counter_map = connection.database[
            "emergencies_counter_per_user_map"
        ]

    async def has_incremented(self, emergency_id: EmergencyId) -> bool:
        document = await self._collection_counter_map.find_one(
            filter={"_id": emergency_id.value}
        )
        return document is not None

    async def increment(
        self, user_id: UserId, emergency_id: EmergencyId
    ) -> EmergenciesCounterPerUser:
        await self._collection_counter_map.insert_one(
            document={"_id": emergency_id.value}
        )

        document = await self._collection_counter.find_one_and_update(
            filter={"_id": user_id.value},
            update={"$inc": {"total": 1}},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )

        emergencies_counter_per_user = EmergenciesCounterPerUser.from_primitives(
            document
        )
        return emergencies_counter_per_user

    async def search(self, user_id: UserId) -> EmergenciesCounterPerUser | None:
        data = await self._collection_counter.find_one()

        if not data:
            return None

        emergencies_counter = EmergenciesCounterPerUser.from_primitives(data)
        return emergencies_counter

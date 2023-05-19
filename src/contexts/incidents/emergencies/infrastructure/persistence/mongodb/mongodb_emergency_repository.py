from contexts.incidents.emergencies.domain.entities import (
    Emergencies,
    Emergency,
    EmergencyRepository,
)
from contexts.incidents.emergencies.domain.value_objects import EmergencyCode
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.criteria import Criteria
from contexts.shared.infrastructure.persistence.mongodb import MongoDbDatabaseConnection


class MongoDbEmergencyRepository(EmergencyRepository):
    def __init__(self, connection: MongoDbDatabaseConnection):
        self._database = connection.database
        self._collection = self._database["emergencies"]

    async def save(self, emergency: Emergency) -> None:
        data = emergency.to_primitives()
        _filter = {"_id": data.pop("id")}
        update = {"$set": data}
        await self._collection.update_one(filter=_filter, update=update, upsert=True)

    async def search(self, emergency_id: EmergencyId) -> Emergency | None:
        _filter = {"_id": emergency_id.value}
        data = await self._collection.find_one(filter=_filter)

        if not data:
            return None

        emergency = Emergency.from_primitives(data)
        return emergency

    async def search_by_criteria(self, criteria: Criteria) -> Emergencies:
        cursor = self._collection.find()

        emergencies_list = [
            Emergency.from_primitives(document) async for document in cursor
        ]

        return Emergencies(items=emergencies_list)

    async def last_code(self) -> EmergencyCode | None:
        return None

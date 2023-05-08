from typing import Any, Dict, Mapping

from typing_extensions import Self

from contexts.incidents.emergencies.domain.value_objects import (
    EmergencyAbscissa,
    EmergencyCode,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.aggregate import AggregateRoot

from .emergency_created_domain_event import EmergencyCreatedDomainEvent


class Emergency(AggregateRoot):
    def __init__(
        self,
        id: EmergencyId,
        code: EmergencyCode,
        abscissa: EmergencyAbscissa,
        user_id: UserId,
    ):
        super().__init__()
        self.id = id
        self.code = code
        self.abscissa = abscissa
        self.user_id = user_id

    @classmethod
    def create(
        cls,
        _id: EmergencyId,
        code: EmergencyCode,
        abscissa: EmergencyAbscissa,
        user_id: UserId,
    ) -> Self:
        emergency = cls(id=_id, code=code, abscissa=abscissa, user_id=user_id)

        emergency.record(
            EmergencyCreatedDomainEvent(
                aggregate_id=_id.value,
                data=dict(
                    code=code.value, abscissa=abscissa.value, user_id=user_id.value
                ),
            )
        )

        return emergency

    def to_primitives(self) -> Dict[str, Any]:
        return {
            "id": self.id.value,
            "code": self.code.value,
            "abscissa": self.abscissa.value,
            "user_id": self.user_id.value,
        }

    @classmethod
    def from_primitives(cls, data: Mapping[str, Any]) -> Self:
        return cls(
            id=EmergencyId(data.get("id") or data["_id"]),
            code=EmergencyCode(data["code"]),
            abscissa=EmergencyAbscissa(data["abscissa"]),
            user_id=UserId(data["user_id"]),
        )

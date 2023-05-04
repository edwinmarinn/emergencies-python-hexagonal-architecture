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
        _id: EmergencyId,
        code: EmergencyCode,
        abscissa: EmergencyAbscissa,
        user_id: UserId,
    ):
        super().__init__()
        self.id = _id
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
        emergency = cls(_id=_id, code=code, abscissa=abscissa, user_id=user_id)

        emergency.record(
            EmergencyCreatedDomainEvent(
                aggregate_id=_id.value,
                data=dict(
                    code=code.value, abscissa=abscissa.value, user_id=user_id.value
                ),
            )
        )

        return emergency

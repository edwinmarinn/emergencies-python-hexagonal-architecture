from contexts.incidents.emergencies.domain.entities import Emergency
from contexts.incidents.emergencies.domain.value_objects import (
    EmergencyAbscissa,
    EmergencyCode,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId


class TestEmergency:
    def test_should_instantiate(self):
        Emergency(
            _id=EmergencyId("bd904284-44f3-4e5b-815a-f5b5a7eb1cbf"),
            code=EmergencyCode("2023.00001"),
            abscissa=EmergencyAbscissa(500),
            user_id=UserId("06daa82b-c733-4c8d-92cd-10074e2dd37a"),
        )

    def test_should_create(self):
        emergency = Emergency.create(
            _id=EmergencyId("bd904284-44f3-4e5b-815a-f5b5a7eb1cbf"),
            code=EmergencyCode("2023.00001"),
            abscissa=EmergencyAbscissa(500),
            user_id=UserId("06daa82b-c733-4c8d-92cd-10074e2dd37a"),
        )

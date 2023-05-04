from contexts.incidents.emergencies.application.find.emergency_response import (
    EmergencyResponse,
)
from contexts.incidents.emergencies.domain.entities import Emergency


class EmergencyResponseConverter:
    def __call__(self, emergency: Emergency) -> EmergencyResponse:
        return EmergencyResponse(
            id=emergency.id.value,
            code=emergency.code.value,
            abscissa=emergency.abscissa.value,
            user_id=emergency.user_id.value,
        )

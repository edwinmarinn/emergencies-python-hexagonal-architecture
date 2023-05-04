from contexts.incidents.emergencies.domain.entities import Emergencies, Emergency

from .emergencies_response import EmergenciesResponse, EmergencyResponse


class EmergenciesResponseConverter:
    @staticmethod
    def converter(emergency: Emergency) -> EmergencyResponse:
        return EmergencyResponse(
            id=emergency.id.value,
            code=emergency.code.value,
            abscissa=emergency.abscissa.value,
            user_id=emergency.user_id.value,
        )

    def __call__(self, emergencies: Emergencies) -> EmergenciesResponse:
        return EmergenciesResponse(list(map(self.converter, emergencies)))

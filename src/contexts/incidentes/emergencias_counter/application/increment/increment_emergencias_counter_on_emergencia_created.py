from typing import List, Type

from contexts.incidentes.emergencias.domain.entities import EmergenciaCreatedDomainEvent
from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber


class IncrementEmergenciasCounterOnEmergenciaCreated(DomainEventSubscriber):
    def __init__(self):
        pass

    @staticmethod
    def subscribed_to() -> List[Type[DomainEvent]]:
        return [EmergenciaCreatedDomainEvent]

    def __call__(self, event: EmergenciaCreatedDomainEvent):
        print("IncrementEmergenciasCounterOnEmergenciaCreated")
        print(event)

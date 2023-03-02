from typing import TypedDict

from contexts.shared.domain.bus.event import DomainEvent


class EmergenciaCreatedDomainEventData(TypedDict):
    code: str
    abscisa: int
    usuario_id: str


class EmergenciaCreatedDomainEvent(DomainEvent):
    def __init__(
        self,
        _id: str,
        data: EmergenciaCreatedDomainEventData,
        event_id: str = None,
        occurred_on: str = None,
    ):
        super().__init__(_id, event_id, occurred_on)
        self._data = data

    @staticmethod
    def event_name() -> str:
        return "emergencia.created"

    @classmethod
    def from_primitives(
        cls,
        aggregate_id: str,
        data: EmergenciaCreatedDomainEventData,
        event_id: str,
        occurred_on: str,
    ) -> "EmergenciaCreatedDomainEvent":
        return cls(
            _id=aggregate_id,
            data=data,
            event_id=event_id,
            occurred_on=occurred_on,
        )

    def to_primitives(self) -> EmergenciaCreatedDomainEventData:
        return self._data

from typing import TypedDict

from typing_extensions import Self

from contexts.shared.domain.bus.event import DomainEvent


class EmergenciesCounterPerUserIncrementedDomainEventData(TypedDict):
    total: int


class EmergenciesCounterPerUserIncrementedDomainEvent(DomainEvent):
    def __init__(
        self,
        aggregate_id: str,
        data: EmergenciesCounterPerUserIncrementedDomainEventData,
        event_id: str | None = None,
        occurred_on: str | None = None,
    ):
        super().__init__(aggregate_id, event_id, occurred_on)
        self._data = data

    @staticmethod
    def event_name() -> str:
        return "emergencies_counter_per_user.incremented"

    @classmethod
    def from_primitives(
        cls,
        aggregate_id: str,
        data: EmergenciesCounterPerUserIncrementedDomainEventData,
        event_id: str,
        occurred_on: str,
    ) -> Self:
        return cls(
            aggregate_id=aggregate_id,
            data=data,
            event_id=event_id,
            occurred_on=occurred_on,
        )

    def to_primitives(self) -> EmergenciesCounterPerUserIncrementedDomainEventData:
        return self._data

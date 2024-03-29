from typing import Any, Type

from typing_extensions import Self

from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber


class FakeDomainEventOne(DomainEvent):
    @classmethod
    def from_primitives(
        cls, aggregate_id: str, data: Any, event_id: str, occurred_on: str
    ) -> Self:
        pass

    @staticmethod
    def event_name() -> str:
        return "fake_domain_event_one"

    def to_primitives(self) -> Any:
        pass


class FakeDomainEventTwo(DomainEvent):
    @classmethod
    def from_primitives(
        cls, aggregate_id: str, data: Any, event_id: str, occurred_on: str
    ) -> Self:
        pass

    @staticmethod
    def event_name() -> str:
        return "fake_domain_event_two"

    def to_primitives(self) -> Any:
        pass


class FakeDomainEventSubscriber(DomainEventSubscriber):
    @staticmethod
    def subscribed_to() -> list[Type[DomainEvent]]:
        return [FakeDomainEventOne, FakeDomainEventTwo]

    async def __call__(self, event: FakeDomainEventOne | FakeDomainEventTwo):
        raise RuntimeError("This works fine!")

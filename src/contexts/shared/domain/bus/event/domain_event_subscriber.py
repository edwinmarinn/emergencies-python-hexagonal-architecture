from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from contexts.shared.domain.bus.event import DomainEvent

DE = TypeVar("DE", bound=DomainEvent)


class DomainEventSubscriber(Generic[DE], ABC):
    @staticmethod
    @abstractmethod
    def subscribed_to() -> List[Type[DomainEvent]]:
        pass

    @abstractmethod
    async def __call__(self, event: DE):
        pass

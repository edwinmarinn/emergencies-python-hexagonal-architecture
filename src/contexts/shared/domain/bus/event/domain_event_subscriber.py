from abc import ABC, abstractmethod
from typing import Any, Dict


class DomainEventSubscriber(ABC):
    @staticmethod
    @abstractmethod
    def subscribed_to() -> Dict[str, Any]:
        pass

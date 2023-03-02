from abc import ABC, abstractmethod
from typing import Dict


class DomainEventSubscriber(ABC):

    @staticmethod
    @abstractmethod
    def subscribed_to() -> Dict[str, any]:
        pass

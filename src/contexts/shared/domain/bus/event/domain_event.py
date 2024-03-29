import datetime
from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import Self

from contexts.incidents.shared.domain.utils.dates import date_to_string
from contexts.shared.domain.value_objects import Uuid


class DomainEvent(ABC):
    def __init__(
        self,
        aggregate_id: str,
        event_id: str | None = None,
        occurred_on: str | None = None,
    ):
        self._aggregate_id = aggregate_id
        self._event_id = event_id or Uuid.random().value
        self._occurred_on = occurred_on or date_to_string(datetime.datetime.now())

    @classmethod
    @abstractmethod
    def from_primitives(
        cls, aggregate_id: str, data: Any, event_id: str, occurred_on: str
    ) -> Self:
        pass

    @staticmethod
    @abstractmethod
    def event_name() -> str:
        pass

    @abstractmethod
    def to_primitives(self) -> Any:
        pass

    @property
    def aggregate_id(self) -> str:
        return self._aggregate_id

    @property
    def event_id(self) -> str:
        return self._event_id

    @property
    def occurred_on(self) -> str:
        return self._occurred_on

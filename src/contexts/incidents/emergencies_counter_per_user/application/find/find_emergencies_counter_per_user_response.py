from dataclasses import dataclass

from contexts.shared.domain.bus.query import Response


@dataclass(frozen=True)
class FindEmergenciesCounterPerUserResponse(Response):
    total: int

from dataclasses import dataclass


@dataclass(frozen=True)
class FindEmergenciesCounterResponse:
    total: int

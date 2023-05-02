from dataclasses import dataclass


@dataclass(frozen=True)
class FindEmergenciasCounterResponse:
    total: int

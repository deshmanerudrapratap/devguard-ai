"""Predictive maintenance models. Implementation comes in a later stage."""

from dataclasses import dataclass


@dataclass
class Forecast:
    repository_id: int
    implemented: bool = False
    message: str = "Predictive maintenance is not implemented yet."


def forecast(repository_id: int) -> Forecast:
    return Forecast(repository_id=repository_id)

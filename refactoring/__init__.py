"""Guarded refactoring pipeline. Implementation comes in a later stage."""

from dataclasses import dataclass


@dataclass
class RefactorPlan:
    repository_id: int
    implemented: bool = False
    message: str = "Refactoring engine is not implemented yet."


def create_plan(repository_id: int) -> RefactorPlan:
    return RefactorPlan(repository_id=repository_id)

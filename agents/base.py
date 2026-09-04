"""Pluggable agent contracts. Concrete agents are not implemented in the foundation stage."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentStatus(str, Enum):
    NOT_IMPLEMENTED = "not_implemented"
    READY = "ready"
    RUNNING = "running"
    FAILED = "failed"


@dataclass(frozen=True)
class AgentContext:
    """Shared input for a future agent run."""

    repository_id: int
    repository_name: str
    local_path: str | None = None
    remote_url: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_id: str
    status: AgentStatus
    message: str
    payload: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Every future DevGuard agent should implement this interface."""

    agent_id: str
    name: str
    status: AgentStatus = AgentStatus.NOT_IMPLEMENTED

    @abstractmethod
    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError

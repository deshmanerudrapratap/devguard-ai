"""Scanner adapters. Concrete scanners will plug in here later."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScanRequest:
    repository_id: int
    local_path: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class ScanResult:
    scanner_id: str
    implemented: bool
    message: str
    findings: list[dict[str, Any]] = field(default_factory=list)


class BaseScanner(ABC):
    scanner_id: str

    @abstractmethod
    def scan(self, request: ScanRequest) -> ScanResult:
        raise NotImplementedError

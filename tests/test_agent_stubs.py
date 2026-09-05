from agents.security import SecurityAgent
from agents.base import AgentContext, AgentStatus
from prediction import forecast
from refactoring import create_plan
from scanners.placeholder import PlaceholderScanner
from scanners.base import ScanRequest


def test_security_agent_is_not_implemented():
    result = SecurityAgent().run(AgentContext(repository_id=1, repository_name="demo"))
    assert result.status == AgentStatus.READY
    assert "total_findings" in result.payload


def test_scanner_returns_no_findings():
    result = PlaceholderScanner().scan(ScanRequest(repository_id=1))
    assert result.implemented is False
    assert result.findings == []


def test_refactor_and_prediction_stubs():
    assert create_plan(1).implemented is False
    assert forecast(1).implemented is False

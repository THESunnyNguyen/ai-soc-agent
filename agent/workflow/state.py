from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvestigationState:
    alert_id: str
    alert_data: dict[str, Any] = field(default_factory=dict)
    runbook_name: str = ""
    findings: list[dict[str, Any]] = field(default_factory=list)
    assessment: str = ""
    summary: str = ""
    recommendation: str = ""  # "false_positive" | "escalate" | "close"
    confidence_score: float = 0.0
    escalation_tier: str = ""
    escalation_reason: str = ""

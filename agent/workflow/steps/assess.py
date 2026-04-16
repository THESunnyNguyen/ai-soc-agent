import json
from pathlib import Path

import structlog
from anthropic import AsyncAnthropic
from mcp import ClientSession

from agent.workflow.state import InvestigationState

log = structlog.get_logger()
_client = AsyncAnthropic()
_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "assess.txt").read_text()


async def run(state: InvestigationState, mcp_session: ClientSession) -> None:
    classification = state.alert_data.get("_classification", {})
    prompt = _PROMPT.format(
        alert_id=state.alert_id,
        alert_type=classification.get("alert_type", "unknown"),
        severity=classification.get("severity", "unknown"),
        findings=json.dumps(state.findings, indent=2),
    )
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    result = json.loads(raw)
    state.assessment = result.get("assessment_detail", "")
    state.confidence_score = float(result.get("confidence_score", 0.0))
    state.recommendation = result.get("recommendation", "escalate")
    state.escalation_tier = result.get("escalation_tier", "")
    state.escalation_reason = result.get("escalation_reason", "")
    state.alert_data["_verdict"] = result.get("verdict", "uncertain")
    log.info(
        "step.assess.done",
        alert_id=state.alert_id,
        verdict=state.alert_data["_verdict"],
        confidence=state.confidence_score,
        recommendation=state.recommendation,
    )

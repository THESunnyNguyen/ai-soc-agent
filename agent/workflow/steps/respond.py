import json
from pathlib import Path

import structlog
from anthropic import AsyncAnthropic
from mcp import ClientSession

from agent.formatter import format_report
from agent.workflow.state import InvestigationState

log = structlog.get_logger()
_client = AsyncAnthropic()
_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "respond.txt").read_text()


async def run(state: InvestigationState, mcp_session: ClientSession) -> None:
    classification = state.alert_data.get("_classification", {})
    prompt = _PROMPT.format(
        alert_id=state.alert_id,
        alert_type=classification.get("alert_type", "unknown"),
        severity=classification.get("severity", "unknown"),
        recommendation=state.recommendation,
        confidence_score=state.confidence_score,
        escalation_tier=state.escalation_tier,
        escalation_reason=state.escalation_reason,
        summary=state.summary,
        assessment_detail=state.assessment,
        key_indicators=json.dumps(state.alert_data.get("_key_indicators", []), indent=2),
    )
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    report_body = response.content[0].text.strip()
    format_report(state, report_body)
    log.info("step.respond.done", alert_id=state.alert_id, recommendation=state.recommendation)

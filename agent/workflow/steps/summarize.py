import json
from pathlib import Path

import structlog
from anthropic import AsyncAnthropic
from mcp import ClientSession

from agent.workflow.state import InvestigationState

log = structlog.get_logger()
_client = AsyncAnthropic()
_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "summarize.txt").read_text()


async def run(state: InvestigationState, mcp_session: ClientSession) -> None:
    classification = state.alert_data.get("_classification", {})
    prompt = _PROMPT.format(
        alert_id=state.alert_id,
        alert_type=classification.get("alert_type", "unknown"),
        severity=classification.get("severity", "unknown"),
        verdict=state.alert_data.get("_verdict", "uncertain"),
        confidence_score=state.confidence_score,
        findings=json.dumps(state.findings, indent=2),
        assessment_detail=state.assessment,
    )
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    state.summary = response.content[0].text.strip()
    log.info("step.summarize.done", alert_id=state.alert_id)

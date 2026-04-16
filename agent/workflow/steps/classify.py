import json
from pathlib import Path

import structlog
from anthropic import AsyncAnthropic
from mcp import ClientSession

from agent.workflow.state import InvestigationState

log = structlog.get_logger()
_client = AsyncAnthropic()
_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "classify.txt").read_text()


async def run(state: InvestigationState, mcp_session: ClientSession) -> None:
    prompt = _PROMPT.format(
        alert_id=state.alert_id,
        alert_data=json.dumps(state.alert_data, indent=2),
    )
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    result = json.loads(raw)
    state.alert_data["_classification"] = {
        "alert_type": result["alert_type"],
        "severity": result["severity"],
        "confidence": result["confidence"],
        "reasoning": result["reasoning"],
    }
    log.info("step.classify.done", alert_id=state.alert_id, alert_type=result["alert_type"], severity=result["severity"])

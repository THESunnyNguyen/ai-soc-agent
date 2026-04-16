import json
from pathlib import Path

import structlog
from anthropic import AsyncAnthropic
from mcp import ClientSession

from agent.workflow.state import InvestigationState

log = structlog.get_logger()
_client = AsyncAnthropic()
_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "select_runbook.txt").read_text()


async def run(state: InvestigationState, mcp_session: ClientSession) -> None:
    classification = state.alert_data.get("_classification", {})
    prompt = _PROMPT.format(
        alert_type=classification.get("alert_type", "unknown"),
        severity=classification.get("severity", "unknown"),
        alert_raw=state.alert_data.get("raw", ""),
    )
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    result = json.loads(raw)
    state.runbook_name = result["runbook_name"]
    log.info("step.select_runbook.done", alert_id=state.alert_id, runbook=state.runbook_name)

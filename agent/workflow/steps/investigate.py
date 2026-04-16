import json
from pathlib import Path
from typing import Any

import structlog
from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool
from mcp import ClientSession

from agent.workflow.state import InvestigationState

log = structlog.get_logger()
_client = AsyncAnthropic()
_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "investigate.txt").read_text()


async def run(state: InvestigationState, mcp_session: ClientSession) -> None:
    classification = state.alert_data.get("_classification", {})

    # Get runbook content via MCP
    rb_result = await mcp_session.call_tool("get_runbook", {"name": state.runbook_name})
    runbook_content = rb_result.content[0].text if rb_result.content else ""
    try:
        rb_data = json.loads(runbook_content)
        runbook_content = rb_data.get("content", runbook_content)
    except (json.JSONDecodeError, AttributeError):
        pass

    # Get alert data via MCP
    alert_result = await mcp_session.call_tool("get_alert", {"alert_id": state.alert_id})
    alert_raw = alert_result.content[0].text if alert_result.content else ""
    try:
        state.alert_data.update(json.loads(alert_raw))
    except (json.JSONDecodeError, AttributeError):
        pass

    prompt = _PROMPT.format(
        alert_id=state.alert_id,
        alert_type=classification.get("alert_type", "unknown"),
        severity=classification.get("severity", "unknown"),
        runbook_content=runbook_content,
    )

    tools_result = await mcp_session.list_tools()
    mcp_tools = [async_mcp_tool(t, mcp_session) for t in tools_result.tools]

    runner = await _client.beta.messages.tool_runner(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
        tools=mcp_tools,
    )

    final_text = ""
    async for message in runner:
        if message.content:
            for block in message.content:
                if hasattr(block, "text"):
                    final_text = block.text

    result = json.loads(final_text.strip())
    state.findings = result.get("findings", [])
    state.alert_data["_key_indicators"] = result.get("key_indicators", [])
    state.alert_data["_investigation_summary"] = result.get("summary", "")
    log.info("step.investigate.done", alert_id=state.alert_id, findings=len(state.findings))

"""
Integration test: full pipeline against alert-001 (brute-force).

Requires a real ANTHROPIC_API_KEY in the environment.
Run with: pytest tests/test_integration.py -v -s
"""
import asyncio
import json
import sys
from pathlib import Path

import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from agent.workflow.state import InvestigationState
from agent.workflow.steps import assess, classify, investigate, respond, select_runbook, summarize


@pytest.mark.asyncio
@pytest.mark.integration
async def test_full_pipeline_brute_force(capsys):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server"],
        env=None,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()

            # Pre-load alert data
            alert_result = await mcp_session.call_tool("get_alert", {"alert_id": "alert-001"})
            alert_raw = alert_result.content[0].text
            alert_data = json.loads(alert_raw)
            assert "error" not in alert_data

            state = InvestigationState(alert_id="alert-001", alert_data=alert_data)

            steps = [
                classify.run,
                select_runbook.run,
                investigate.run,
                assess.run,
                summarize.run,
                respond.run,
            ]
            for step_fn in steps:
                await step_fn(state, mcp_session)

            # Verify state is populated end-to-end
            assert state.alert_data.get("_classification", {}).get("alert_type") == "brute-force"
            assert state.runbook_name == "brute-force"
            assert len(state.findings) > 0
            assert state.confidence_score > 0.0
            assert state.recommendation in ("false_positive", "escalate", "close")
            assert state.summary != ""

            # Verify report printed to stdout
            captured = capsys.readouterr()
            assert "→ Awaiting analyst decision." in captured.out

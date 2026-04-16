#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys

import structlog
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from agent.workflow.pipeline import run_pipeline
from agent.workflow.state import InvestigationState

log = structlog.get_logger()


async def main(alert_id: str) -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server"],
        env=None,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()
            log.info("mcp_server.connected", alert_id=alert_id)

            # Pre-load alert data before pipeline starts
            alert_result = await mcp_session.call_tool("get_alert", {"alert_id": alert_id})
            alert_raw = alert_result.content[0].text if alert_result.content else "{}"
            try:
                alert_data = json.loads(alert_raw)
            except json.JSONDecodeError:
                alert_data = {}

            if "error" in alert_data:
                print(f"Error: {alert_data['error']}", file=sys.stderr)
                sys.exit(1)

            state = InvestigationState(alert_id=alert_id, alert_data=alert_data)

            # Run the full 6-step pipeline
            from agent.workflow.steps import assess, classify, investigate, respond, select_runbook, summarize
            steps = [
                ("classify", classify.run),
                ("select_runbook", select_runbook.run),
                ("investigate", investigate.run),
                ("assess", assess.run),
                ("summarize", summarize.run),
                ("respond", respond.run),
            ]
            for step_name, step_fn in steps:
                log.info("pipeline.step.start", step=step_name, alert_id=alert_id)
                try:
                    await step_fn(state, mcp_session)
                    log.info("pipeline.step.done", step=step_name)
                except Exception as exc:
                    log.error("pipeline.step.failed", step=step_name, error=str(exc))
                    raise


def cli() -> None:
    parser = argparse.ArgumentParser(description="AI SOC Agent — investigate a security alert")
    parser.add_argument("--alert", required=True, metavar="ALERT_ID", help="Alert ID to investigate")
    args = parser.parse_args()
    asyncio.run(main(args.alert))


if __name__ == "__main__":
    cli()

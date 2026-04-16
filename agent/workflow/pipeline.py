import structlog
from mcp import ClientSession

from agent.workflow.state import InvestigationState
from agent.workflow.steps import assess, classify, investigate, respond, select_runbook, summarize

log = structlog.get_logger()


async def run_pipeline(alert_id: str, mcp_session: ClientSession) -> InvestigationState:
    state = InvestigationState(alert_id=alert_id)
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
            log.info("pipeline.step.done", step=step_name, alert_id=alert_id)
        except Exception as exc:
            log.error("pipeline.step.failed", step=step_name, alert_id=alert_id, error=str(exc))
            raise

    return state

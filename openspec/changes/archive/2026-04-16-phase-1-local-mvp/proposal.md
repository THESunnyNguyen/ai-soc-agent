## Why

The ai-soc-agent has a full system spec but no running code. Phase 1 delivers the first end-to-end functional slice — a locally runnable investigation pipeline that ingests a sample alert, runs it through all 6 steps with real Claude calls, and prints an adaptive formatted report for a human SOC analyst to review.

## What Changes

- Introduce the 6-step agent pipeline (classify → select_runbook → investigate → assess → summarize → respond)
- Implement all 5 MCP tools (list_alerts, get_alert, search_events, get_entity_context, enrich_ip, get_runbook) backed by a JSON file store
- Add hardcoded sample alert data in `data/samples/alerts.json`
- Add prompt templates for all 6 pipeline steps
- Add a CLI entry point (`run_agent.py`) for local invocation
- The respond step produces an adaptive stdout report — tone, depth, and call-to-action vary by confidence and escalation status; human analyst has final say

## Capabilities

### New Capabilities
- `agent-pipeline`: 6-step investigation pipeline orchestrated via Anthropic SDK, with shared state passed between steps
- `mcp-tools`: All 5 MCP tools exposed over stdio transport, validated with pydantic
- `json-store`: File-backed alert and event storage with abstract base for future PostgreSQL upgrade
- `cli-runner`: Entry point for triggering an investigation by alert ID from the command line
- `report-formatter`: Adaptive stdout report formatted by confidence level and escalation recommendation; awaits human decision

### Modified Capabilities
- `agent`: Adding step 6 (respond) and full prompt templates — spec-level pipeline definition changes
- `mcp-server`: Pinning transport to stdio for Phase 1; all 5 tools now have concrete implementations

## Impact

- New top-level files: `run_agent.py`, `data/samples/alerts.json`, `runbooks/*.md`
- New packages: `agent/`, `mcp_server/`
- Dependencies: `anthropic`, `mcp`, `pydantic`, `structlog`, `pytest`, `pytest-asyncio`
- No Docker, no Discord, no PostgreSQL in Phase 1

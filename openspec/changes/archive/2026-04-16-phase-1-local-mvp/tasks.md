## 1. Project Scaffolding

- [x] 1.1 Create `requirements.txt` with: anthropic, mcp, pydantic, structlog, pytest, pytest-asyncio
- [x] 1.2 Create package directories: `agent/workflow/steps/`, `agent/prompts/`, `mcp_server/storage/`, `mcp_server/tools/`, `data/samples/`, `runbooks/`
- [x] 1.3 Add `__init__.py` files to all Python packages

## 2. Sample Data

- [x] 2.1 Create `data/samples/alerts.json` with 3 alerts: brute-force, lateral-movement, data-exfil
- [x] 2.2 Include associated events, entity context, and mock IP enrichment data for each alert in the JSON file

## 3. Runbooks

- [x] 3.1 Create `runbooks/brute-force.md` investigation playbook
- [x] 3.2 Create `runbooks/lateral-movement.md` investigation playbook
- [x] 3.3 Create `runbooks/data-exfil.md` investigation playbook

## 4. Storage Layer

- [x] 4.1 Implement `mcp_server/storage/base.py` — `StorageBase` abstract class with `get_alerts`, `get_alert`, `search_events`, `get_entity_context`, `get_enrichment`
- [x] 4.2 Implement `mcp_server/storage/json_store.py` — `JsonStore` implementing `StorageBase`, loads `alerts.json` at init
- [x] 4.3 Add stub `mcp_server/storage/postgres_store.py` — raises `NotImplementedError` for all methods

## 5. MCP Tools

- [x] 5.1 Implement `mcp_server/tools/alerts.py` — `list_alerts` and `get_alert` tools with pydantic validation
- [x] 5.2 Implement `mcp_server/tools/events.py` — `search_events` tool with pydantic validation
- [x] 5.3 Implement `mcp_server/tools/context.py` — `get_entity_context` tool with pydantic validation
- [x] 5.4 Implement `mcp_server/tools/enrichment.py` — `enrich_ip` tool returning mock data, with pydantic validation
- [x] 5.5 Implement `mcp_server/tools/runbooks.py` — `get_runbook` tool reading from `runbooks/`
- [x] 5.6 Create `mcp_server/server.py` — wire all tools into MCP server, stdio transport

## 6. Agent Pipeline State & Orchestrator

- [x] 6.1 Implement `agent/workflow/state.py` — `InvestigationState` dataclass with all fields: alert_id, alert_data, runbook_name, findings, assessment, summary, recommendation, confidence_score
- [x] 6.2 Implement `agent/workflow/pipeline.py` — runs steps 1–6 in order, passes state, halts and logs on exception

## 7. Prompt Templates

- [x] 7.1 Create `agent/prompts/classify.txt`
- [x] 7.2 Create `agent/prompts/select_runbook.txt`
- [x] 7.3 Create `agent/prompts/investigate.txt`
- [x] 7.4 Create `agent/prompts/assess.txt`
- [x] 7.5 Create `agent/prompts/summarize.txt`
- [x] 7.6 Create `agent/prompts/respond.txt`

## 8. Pipeline Steps

- [x] 8.1 Implement `agent/workflow/steps/classify.py` — calls Claude with classify prompt, populates alert type/severity on state
- [x] 8.2 Implement `agent/workflow/steps/select_runbook.py` — calls Claude with select_runbook prompt, sets runbook_name on state
- [x] 8.3 Implement `agent/workflow/steps/investigate.py` — calls Claude with investigate prompt, uses MCP tools, populates findings on state
- [x] 8.4 Implement `agent/workflow/steps/assess.py` — calls Claude with assess prompt, sets assessment and confidence_score on state
- [x] 8.5 Implement `agent/workflow/steps/summarize.py` — calls Claude with summarize prompt, sets summary on state
- [x] 8.6 Implement `agent/workflow/steps/respond.py` — calls Claude with respond prompt, sets recommendation on state, invokes report formatter

## 9. Report Formatter

- [x] 9.1 Implement `agent/formatter.py` — adaptive stdout report: high-confidence false positive (brief), low-confidence/escalate (full detail), mid-range (balanced); all end with "→ Awaiting analyst decision."
- [x] 9.2 Ensure escalation output includes tier label (e.g., "Tier 2 — Threat Hunter") and one-sentence reason

## 10. CLI Entry Point

- [x] 10.1 Implement `run_agent.py` — accepts `--alert <id>`, launches MCP server subprocess, runs pipeline, terminates subprocess
- [x] 10.2 Handle missing `--alert` argument with usage error and non-zero exit

## 11. Tests

- [x] 11.1 Write unit tests for `JsonStore` — covers all 5 interface methods with sample data
- [x] 11.2 Write unit tests for each MCP tool — valid input, invalid input, not-found cases
- [x] 11.3 Write unit tests for `formatter.py` — all 3 confidence/recommendation branches
- [x] 11.4 Write an integration test that runs the full pipeline against `alert-001` (brute-force) using real Claude API

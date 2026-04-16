# MCP Server Spec

## Purpose
Exposes tools to the agent. Transport selectable via MCP_TRANSPORT env var
(stdio or HTTP).

## Tools (current)
- `alerts.py` — list_alerts, get_alert
- `events.py` — search_events
- `context.py` — get_entity_context
- `enrichment.py` — enrich_ip
- `runbooks.py` — get_runbook

## Storage
- Phase 1–3: JSON file store (`storage/json_store.py`)
- Phase 4+: PostgreSQL (`storage/postgres_store.py`)
- Abstract interface: `storage/base.py`

## Requirements
- MUST support both stdio and HTTP transport
- MUST validate inputs/outputs with pydantic
- MUST be independently containerizable
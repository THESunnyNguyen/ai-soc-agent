# ai-soc-agent

An AI-powered Security Operations Center (SOC) agent that investigates alerts through a 6-step pipeline using Claude and the Model Context Protocol (MCP).

## Overview

The agent ingests a security alert, runs it through a structured investigation pipeline, and produces an adaptive report for a human SOC analyst to review. The analyst always has final say — the agent never takes autonomous action.

### Investigation Pipeline

```
classify → select_runbook → investigate → assess → summarize → respond
```

1. **classify** — determine alert type and severity
2. **select_runbook** — choose the appropriate investigation playbook
3. **investigate** — gather evidence via MCP tools (events, entity context, IP enrichment)
4. **assess** — evaluate findings and assign confidence score
5. **summarize** — produce a human-readable summary
6. **respond** — format an adaptive report and surface escalation recommendation

### MCP Tools

The MCP server exposes 6 tools over stdio transport:

| Tool | Description |
|---|---|
| `list_alerts` | Return all alerts from the store |
| `get_alert` | Fetch a single alert by ID |
| `search_events` | Keyword search over raw events |
| `get_entity_context` | Look up context for an IP, hostname, or user |
| `enrich_ip` | Return threat intel enrichment for an IP (mock in Phase 1) |
| `get_runbook` | Read a Markdown investigation runbook |

## Quickstart

### Prerequisites

- Python 3.11+
- An Anthropic API key

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
export ANTHROPIC_API_KEY=sk-...
python run_agent.py --alert alert-001
```

Available sample alert IDs: `alert-001` (brute-force), `alert-002` (lateral-movement), `alert-003` (data-exfil).

### Test

```bash
pytest
```

## Project Structure

```
ai-soc-agent/
├── agent/
│   ├── workflow/
│   │   ├── steps/          # One file per pipeline step
│   │   ├── pipeline.py     # Orchestrator
│   │   └── state.py        # Shared InvestigationState dataclass
│   ├── prompts/            # Plain .txt prompt templates
│   └── formatter.py        # Adaptive report formatter
├── mcp_server/
│   ├── tools/              # One file per MCP tool
│   ├── storage/            # StorageBase, JsonStore, PostgresStore (stub)
│   └── server.py           # MCP server entry point (stdio)
├── data/samples/           # Sample alert data (JSON)
├── runbooks/               # Markdown investigation playbooks
├── tests/                  # Unit + integration tests
└── run_agent.py            # CLI entry point
```

## Architecture

- **Agent** — orchestrates the pipeline via the Anthropic SDK; prompt templates are plain `.txt` files
- **MCP Server** — exposes tools over stdio; launched as a subprocess by `run_agent.py`
- **Storage** — abstract `StorageBase` with a JSON file backend (Phase 1); PostgreSQL backend planned for Phase 4
- **Report** — adaptive stdout output; tone and depth vary by confidence score and escalation status

## Roadmap

| Phase | Description |
|---|---|
| 1 (current) | Local MVP — CLI runner, JSON store, stdout report |
| 2 | HTTP transport, Docker, persistent storage |
| 3 | Discord bot UI |
| 4 | PostgreSQL backend, multi-tenant support |

## Contributing

See `openspec/AGENTS.md` for the spec workflow. All changes larger than a bug fix require an OpenSpec proposal before implementation.

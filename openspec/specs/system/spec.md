# System Spec — ai-soc-agent

## Overview
AI-powered Security Operations Center agent. Ingests alerts, runs
structured investigations via runbooks, and surfaces results through a
Discord bot.

## Stack
- Language: Python 3.12+
- MCP server: `mcp` Python SDK
- Agent: `anthropic` Python SDK
- Discord: `discord.py`
- Data validation: `pydantic`
- Logging: `structlog`
- Testing: `pytest` + `pytest-asyncio`
- Containers: Docker + Docker Compose
- Orchestration: k3s on OCI free tier (ARM A1)
- CI/CD: GitHub Actions
- K8s packaging: Helm (Phase 7)
- Cloud: Oracle Cloud Free Tier

## Services
- `mcp_server/` — exposes tools to the agent over stdio or HTTP
- `agent/` — orchestrates the 6-step investigation pipeline
- `discord_bot/` — user-facing interface for triggering and viewing investigations

## Repo Layout
- `data/` — generators, samples, schema, migrations
- `runbooks/` — Markdown investigation playbooks
- `infra/` — docker-compose and k8s manifests
- `docs/` — architecture and runbook guide, Discord Bot  →  Agent (via direct call or queue) Agent        →  MCP Server (via stdio or HTTP) MCP Server   →  Storage (JSON or Postgres) MCP Server   →  Runbooks (filesystem reads)
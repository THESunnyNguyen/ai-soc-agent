# ai-soc-agent

## What this project is
AI SOC agent lab. MCP server exposes tools. Agent runs a 6-step investigation
pipeline. Discord bot is the user interface. See openspec/AGENTS.md for the
full spec workflow.

## Key conventions
- Always read openspec/AGENTS.md before proposing or implementing anything
- Storage changes must update both json_store.py and postgres_store.py via base.py
- Agent steps live in agent/workflow/steps/ — one file per step, no exceptions
- Prompt templates are plain .txt files in agent/prompts/ — not f-strings in code
- structlog for all logging — no print() or logging.getLogger()
- pytest-asyncio for all async tests

## What NOT to do
- Do not write business logic in discord_bot/ — it calls agent/, nothing more
- Do not hardcode alert IDs, API keys, or endpoints anywhere
- Do not skip the openspec proposal step for anything larger than a bug fix
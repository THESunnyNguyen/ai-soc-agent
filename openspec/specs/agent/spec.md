# Agent Spec

## Purpose
Orchestrates the 6-step investigation pipeline using the Anthropic SDK.

## Pipeline Steps (in order)
1. `classify.py` — determine alert type / severity
2. `select_runbook.py` — choose the appropriate runbook
3. `investigate.py` — execute investigation steps
4. `assess.py` — evaluate findings
5. `summarize.py` — produce human-readable summary

## State
- `workflow/state.py` — investigation state dataclass passed between steps
- `workflow/pipeline.py` — top-level orchestrator

## Prompts
- Stored as plain text files in `prompts/`, one per step

## Requirements
- MUST be independently containerizable
- MUST support file-based memory (Phase 1–3)
- SHOULD support postgres-backed memory (Phase 4+)
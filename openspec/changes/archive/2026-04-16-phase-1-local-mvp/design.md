## Context

No code exists yet. This design covers the first runnable slice of the ai-soc-agent: a locally executable investigation pipeline with a JSON-backed MCP server, invoked from the CLI. Discord, Docker, and PostgreSQL are all deferred.

## Goals / Non-Goals

**Goals:**
- All 6 pipeline steps functional with real Claude API calls
- All 5 MCP tools implemented and reachable over stdio
- JSON file store with abstract base ready for PostgreSQL swap
- Adaptive stdout report from the respond step
- End-to-end test with a sample alert

**Non-Goals:**
- Discord integration (Phase 2)
- HTTP MCP transport (Phase 1 uses stdio only)
- PostgreSQL (Phase 4+)
- Docker / container packaging (Phase 2+)
- Authentication, rate limiting, multi-user support

## Decisions

### 1. MCP transport: stdio only
**Decision:** Phase 1 uses stdio exclusively; `MCP_TRANSPORT` env var reserved for later.  
**Rationale:** stdio is simpler to run locally and sufficient for a single-process CLI invocation. HTTP adds operational complexity (port binding, lifecycle) with no Phase 1 benefit.  
**Alternative considered:** Start with HTTP from day one — rejected because it requires a server process separate from the CLI runner.

### 2. Agent ↔ MCP: in-process vs subprocess
**Decision:** MCP server runs as a subprocess launched by the agent, communicating over stdio.  
**Rationale:** Matches the MCP SDK's standard stdio pattern. Keeps the two services independently containerizable later.  
**Alternative considered:** Import MCP tools as plain Python functions — simpler but defeats the purpose of the MCP abstraction and makes the later HTTP switch harder.

### 3. Storage: abstract base from day one
**Decision:** `storage/base.py` defines the interface; `json_store.py` is the only Phase 1 implementation.  
**Rationale:** The PostgreSQL upgrade (Phase 4) is known and certain. Designing the abstract base now costs little and avoids a refactor later.  
**Alternative considered:** Skip the abstraction for Phase 1 — rejected because it would require touching every MCP tool when swapping stores.

### 4. Pipeline state: shared dataclass
**Decision:** A single `InvestigationState` dataclass in `workflow/state.py` is passed through all 6 steps and mutated in place.  
**Rationale:** Simple, type-safe, easy to serialize for future persistence. Avoids implicit coupling between steps.  
**Alternative considered:** Each step returns a dict merged into a global dict — rejected due to lack of type safety and discoverability.

### 5. Prompts: plain .txt files, no f-strings in code
**Decision:** All 6 prompt templates live in `agent/prompts/` as `.txt` files; variables injected at runtime via `.format()`.  
**Rationale:** Prompts change frequently. Keeping them out of code means no redeploy for prompt tuning. Consistent with CLAUDE.md convention.

### 6. Respond step: recommendation only, no autonomous action
**Decision:** The respond step outputs a formatted recommendation (escalate / close / false positive) with reasoning. The human SOC analyst has final say. No action is taken by the agent.  
**Rationale:** Avoids false escalations in Phase 1 where accuracy is best-effort. Builds trust before introducing automation.

### 7. Report formatter: confidence-adaptive output
**Decision:** The formatter adjusts tone, depth, and call-to-action based on confidence score and escalation status:
- High confidence false positive (≥80%): brief summary, key exonerating evidence, "Recommendation: Close"
- Low confidence / suspicious (≤50%): full detail, all indicators, "Recommendation: Escalate to Tier N"
- Mid-range: balanced summary with uncertainty noted

All reports end with "→ Awaiting analyst decision."  
**Rationale:** Analysts make faster, better decisions when the report matches the situation. Dense reports for obvious false positives waste time.

### 8. Sample data: hardcoded JSON, not a generator
**Decision:** `data/samples/alerts.json` contains a small fixed set of sample alerts and events.  
**Rationale:** Sufficient for Phase 1 validation. A generator adds complexity with no Phase 1 payoff. The JSON store can be seeded from this file at startup.

## Risks / Trade-offs

- **Claude API latency per step** → 6 sequential LLM calls means ~10-30s end-to-end. Acceptable for Phase 1; parallelism is a later optimization.
- **Prompt quality is best-effort** → Classification and assessment accuracy will be rough initially. Documented as expected; iterative improvement is the plan.
- **stdio subprocess is fragile on Windows** → MCP stdio process management can behave differently on Windows. Mitigated by targeting Linux/Mac for development; Docker resolves this in Phase 2.
- **JSON store has no concurrency** → Single-file JSON is not safe for concurrent writes. Acceptable since Phase 1 is single-process CLI only.

## Migration Plan

Phase 1 is greenfield — no migration needed. To run:
```
pip install -r requirements.txt
python run_agent.py --alert <alert-id>
```

Phase 4 PostgreSQL upgrade: swap `json_store.py` for `postgres_store.py` behind `base.py` — no changes to MCP tool code required.

## Open Questions

- What alert types should the sample data cover? (suggested: brute force, lateral movement, data exfil — one per confidence tier)
- Should runbooks be per alert-type or per severity? (suggested: per alert-type for Phase 1)

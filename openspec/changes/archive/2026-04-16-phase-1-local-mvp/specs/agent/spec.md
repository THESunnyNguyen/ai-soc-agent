## MODIFIED Requirements

### Requirement: Pipeline steps definition
The agent pipeline SHALL consist of exactly 6 steps in this order:
1. `classify.py` — determine alert type and severity
2. `select_runbook.py` — choose the appropriate runbook
3. `investigate.py` — execute investigation steps via MCP tools
4. `assess.py` — evaluate findings
5. `summarize.py` — produce human-readable summary
6. `respond.py` — format adaptive report and surface escalation recommendation

Each step SHALL have a corresponding prompt template in `agent/prompts/<step_name>.txt`.

#### Scenario: All 6 steps present
- **WHEN** the pipeline is instantiated
- **THEN** all 6 step files exist in `agent/workflow/steps/` and all 6 prompt files exist in `agent/prompts/`

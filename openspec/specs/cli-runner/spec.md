# CLI Runner Spec

## Purpose
Command-line entry point for triggering an investigation by alert ID, managing the MCP server subprocess lifecycle.

## Requirements

### Requirement: CLI entry point
A `run_agent.py` script SHALL exist at the repo root. It SHALL accept `--alert <alert-id>` as a required argument and invoke the full 6-step pipeline against that alert ID.

#### Scenario: Valid alert ID
- **WHEN** `python run_agent.py --alert alert-001` is run
- **THEN** the pipeline executes all 6 steps and prints the formatted report to stdout

#### Scenario: Missing alert ID argument
- **WHEN** `python run_agent.py` is run with no arguments
- **THEN** the script prints a usage error and exits with a non-zero status code

### Requirement: MCP server launched as subprocess
`run_agent.py` SHALL start the MCP server as a subprocess over stdio before invoking the pipeline, and SHALL terminate it cleanly after the pipeline completes or errors.

#### Scenario: MCP server lifecycle
- **WHEN** `run_agent.py` runs
- **THEN** the MCP server subprocess is started before the first pipeline step and terminated after the last step (or on error)

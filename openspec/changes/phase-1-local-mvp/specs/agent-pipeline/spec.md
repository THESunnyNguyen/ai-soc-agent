## ADDED Requirements

### Requirement: Pipeline executes all 6 steps in order
The agent SHALL execute steps in this fixed sequence: classify → select_runbook → investigate → assess → summarize → respond. Each step receives the shared `InvestigationState` and MAY mutate it. If any step raises an unhandled exception, the pipeline SHALL halt and log the error via structlog.

#### Scenario: Successful end-to-end run
- **WHEN** `run_agent.py` is invoked with a valid alert ID
- **THEN** all 6 steps execute in order, state is passed through each, and a formatted report is printed to stdout

#### Scenario: Step failure halts pipeline
- **WHEN** any pipeline step raises an exception
- **THEN** the pipeline halts, logs the step name and error, and exits with a non-zero status code

### Requirement: Shared investigation state
The pipeline SHALL use a single `InvestigationState` dataclass defined in `workflow/state.py` that is passed to every step. The state SHALL include at minimum: alert_id, alert_data, runbook_name, findings, assessment, summary, recommendation, confidence_score.

#### Scenario: State populated by classify step
- **WHEN** the classify step completes
- **THEN** `InvestigationState.alert_data` and a severity/type classification are populated on the state object

### Requirement: Each step implemented in its own file
Each pipeline step SHALL live in `agent/workflow/steps/<step_name>.py` with no business logic in any other location.

#### Scenario: Step isolation
- **WHEN** a developer adds a new step
- **THEN** they create a single new file in `agent/workflow/steps/` with no changes to other step files

### Requirement: All steps make real Claude API calls
Every step SHALL use the Anthropic SDK to call Claude. No step SHALL be a stub or return hardcoded output in production code.

#### Scenario: Classify step calls Claude
- **WHEN** the classify step runs
- **THEN** it sends the alert data to Claude using a prompt from `agent/prompts/classify.txt` and stores the response on the state

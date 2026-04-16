# MCP Tools Spec

## Purpose
Defines the contract for all MCP tools exposed by the server, including inputs, outputs, and error handling.

## Requirements

### Requirement: list_alerts tool
The MCP server SHALL expose a `list_alerts` tool that returns all alerts from the store. Results SHALL be validated with pydantic before being returned.

#### Scenario: Returns all alerts
- **WHEN** the agent calls `list_alerts` with no filters
- **THEN** the tool returns a list of all alert objects from the JSON store

### Requirement: get_alert tool
The MCP server SHALL expose a `get_alert(alert_id: str)` tool that returns a single alert by ID. If the alert does not exist, the tool SHALL return an error response (not raise an exception).

#### Scenario: Alert found
- **WHEN** the agent calls `get_alert` with a valid alert ID
- **THEN** the tool returns the full alert object

#### Scenario: Alert not found
- **WHEN** the agent calls `get_alert` with an unknown alert ID
- **THEN** the tool returns an error response indicating the alert was not found

### Requirement: search_events tool
The MCP server SHALL expose a `search_events(query: str)` tool that searches events by keyword match against the JSON store. Returns a list of matching event objects.

#### Scenario: Events found
- **WHEN** the agent calls `search_events` with a keyword present in sample data
- **THEN** the tool returns matching event objects

#### Scenario: No events found
- **WHEN** the agent calls `search_events` with a keyword that matches nothing
- **THEN** the tool returns an empty list

### Requirement: get_entity_context tool
The MCP server SHALL expose a `get_entity_context(entity: str)` tool that returns contextual information about a named entity (IP, hostname, user) from the store.

#### Scenario: Entity found
- **WHEN** the agent calls `get_entity_context` with a known entity
- **THEN** the tool returns the entity's context record

### Requirement: enrich_ip tool
The MCP server SHALL expose an `enrich_ip(ip: str)` tool. In Phase 1, this SHALL return a mocked enrichment response from the JSON store (no live threat intel calls).

#### Scenario: IP enrichment returns mock data
- **WHEN** the agent calls `enrich_ip` with any IP address
- **THEN** the tool returns a mock enrichment record from the sample data store

### Requirement: get_runbook tool
The MCP server SHALL expose a `get_runbook(name: str)` tool that reads and returns the contents of a Markdown runbook file from `runbooks/`.

#### Scenario: Runbook found
- **WHEN** the agent calls `get_runbook` with a valid runbook name
- **THEN** the tool returns the full Markdown content of that runbook

#### Scenario: Runbook not found
- **WHEN** the agent calls `get_runbook` with an unknown name
- **THEN** the tool returns an error response

### Requirement: All tool inputs/outputs validated with pydantic
Every MCP tool SHALL validate its inputs and outputs using pydantic models. Invalid inputs SHALL return a structured error, not raise an unhandled exception.

#### Scenario: Invalid input to tool
- **WHEN** the agent calls a tool with a missing required parameter
- **THEN** the tool returns a pydantic validation error response

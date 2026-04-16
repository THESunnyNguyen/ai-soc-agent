## ADDED Requirements

### Requirement: Abstract storage base
A `StorageBase` abstract class SHALL be defined in `mcp_server/storage/base.py`. All store implementations SHALL subclass it. The interface SHALL define at minimum: `get_alerts()`, `get_alert(id)`, `search_events(query)`, `get_entity_context(entity)`, `get_enrichment(ip)`.

#### Scenario: JSON store implements base
- **WHEN** `JsonStore` is instantiated
- **THEN** it satisfies the full `StorageBase` interface without raising `NotImplementedError`

### Requirement: JSON file store implementation
`mcp_server/storage/json_store.py` SHALL implement `StorageBase` by reading from `data/samples/alerts.json` at startup. The file SHALL be loaded once into memory; no live re-reads during a pipeline run.

#### Scenario: Store loads sample data
- **WHEN** `JsonStore` is initialized with the path to `alerts.json`
- **THEN** all alerts and events from the file are accessible via the store interface

### Requirement: Sample data file
`data/samples/alerts.json` SHALL contain at least 3 sample alerts covering distinct scenarios: one brute force, one lateral movement, one data exfiltration. Each alert SHALL include associated events and entity context sufficient for all 5 MCP tools to return meaningful data.

#### Scenario: Sample data covers all tool queries
- **WHEN** the pipeline runs against any sample alert ID
- **THEN** all 5 MCP tools return non-empty responses using only the sample data

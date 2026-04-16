## MODIFIED Requirements

### Requirement: Phase 1 transport is stdio only
In Phase 1, the MCP server SHALL use stdio transport exclusively. The `MCP_TRANSPORT` env var is reserved for future phases and SHALL be ignored in Phase 1. HTTP transport is not supported until Phase 2.

#### Scenario: MCP server starts over stdio
- **WHEN** the MCP server is launched as a subprocess by `run_agent.py`
- **THEN** it communicates over stdio without requiring any port binding or network configuration

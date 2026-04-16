import os
from pathlib import Path
from typing import Any

import structlog
from mcp.server.fastmcp import FastMCP

from mcp_server.storage.json_store import JsonStore
from mcp_server.tools import alerts, context, enrichment, events, runbooks

log = structlog.get_logger()

DATA_PATH = Path(__file__).parent.parent / "data" / "samples" / "alerts.json"

mcp = FastMCP("ai-soc-agent")
_store = JsonStore(DATA_PATH)


@mcp.tool()
def list_alerts() -> list[dict[str, Any]]:
    """List all alerts in the store."""
    return alerts.list_alerts(_store)


@mcp.tool()
def get_alert(alert_id: str) -> dict[str, Any]:
    """Get a single alert by ID."""
    return alerts.get_alert(_store, alert_id)


@mcp.tool()
def search_events(query: str) -> list[dict[str, Any]]:
    """Search events by keyword."""
    return events.search_events(_store, query)


@mcp.tool()
def get_entity_context(entity: str) -> dict[str, Any]:
    """Get context for an entity (IP, hostname, or username)."""
    return context.get_entity_context(_store, entity)


@mcp.tool()
def enrich_ip(ip: str) -> dict[str, Any]:
    """Get threat intelligence enrichment for an IP address."""
    return enrichment.enrich_ip(_store, ip)


@mcp.tool()
def get_runbook(name: str) -> dict[str, Any]:
    """Get the contents of an investigation runbook by name."""
    return runbooks.get_runbook(name)


if __name__ == "__main__":
    log.info("mcp_server.starting", transport="stdio")
    mcp.run(transport="stdio")

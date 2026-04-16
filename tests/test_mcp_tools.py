from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server.storage.json_store import JsonStore
from mcp_server.tools import alerts, context, enrichment, events
from mcp_server.tools.runbooks import get_runbook

DATA_PATH = Path(__file__).parent.parent / "data" / "samples" / "alerts.json"


@pytest.fixture
def store() -> JsonStore:
    return JsonStore(DATA_PATH)


# --- alerts ---

def test_list_alerts(store):
    result = alerts.list_alerts(store)
    assert len(result) == 3


def test_get_alert_valid(store):
    result = alerts.get_alert(store, "alert-001")
    assert result["id"] == "alert-001"
    assert "error" not in result


def test_get_alert_not_found(store):
    result = alerts.get_alert(store, "alert-999")
    assert "error" in result


def test_get_alert_empty_id(store):
    # Empty string passes pydantic but returns not-found
    result = alerts.get_alert(store, "")
    assert "error" in result


# --- events ---

def test_search_events_valid(store):
    result = events.search_events(store, "ssh")
    assert isinstance(result, list)
    assert len(result) > 0


def test_search_events_no_match(store):
    result = events.search_events(store, "zzz-no-match-zzz")
    assert result == []


# --- context ---

def test_get_entity_context_valid(store):
    result = context.get_entity_context(store, "jsmith")
    assert "error" not in result
    assert result["type"] == "user"


def test_get_entity_context_not_found(store):
    result = context.get_entity_context(store, "nobody")
    assert "error" in result


# --- enrichment ---

def test_enrich_ip_known(store):
    result = enrichment.enrich_ip(store, "185.220.101.45")
    assert "error" not in result
    assert result["reputation_score"] == 92


def test_enrich_ip_unknown(store):
    result = enrichment.enrich_ip(store, "1.2.3.4")
    assert "error" not in result
    assert result["reputation_score"] == 0


# --- runbooks ---

def test_get_runbook_valid():
    result = get_runbook("brute-force")
    assert "error" not in result
    assert "content" in result
    assert "Brute Force" in result["content"]


def test_get_runbook_not_found():
    result = get_runbook("nonexistent-runbook")
    assert "error" in result

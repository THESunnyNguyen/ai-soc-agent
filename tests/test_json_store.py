from pathlib import Path

import pytest

from mcp_server.storage.json_store import JsonStore

DATA_PATH = Path(__file__).parent.parent / "data" / "samples" / "alerts.json"


@pytest.fixture
def store() -> JsonStore:
    return JsonStore(DATA_PATH)


def test_get_alerts_returns_all(store):
    alerts = store.get_alerts()
    assert len(alerts) == 3
    assert all("id" in a for a in alerts)


def test_get_alert_found(store):
    alert = store.get_alert("alert-001")
    assert alert is not None
    assert alert["id"] == "alert-001"
    assert alert["type"] == "brute-force"


def test_get_alert_not_found(store):
    alert = store.get_alert("alert-999")
    assert alert is None


def test_search_events_found(store):
    results = store.search_events("brute-force")
    assert len(results) > 0


def test_search_events_by_alert_id(store):
    results = store.search_events("alert-002")
    assert len(results) >= 3
    assert all("evt-002" in r["id"] for r in results)


def test_search_events_no_match(store):
    results = store.search_events("zzz-no-match-zzz")
    assert results == []


def test_get_entity_context_found(store):
    ctx = store.get_entity_context("185.220.101.45")
    assert ctx is not None
    assert ctx["known_malicious"] is True


def test_get_entity_context_not_found(store):
    ctx = store.get_entity_context("999.999.999.999")
    assert ctx is None


def test_get_enrichment_found(store):
    result = store.get_enrichment("185.220.101.45")
    assert result is not None
    assert result["reputation_score"] == 92


def test_get_enrichment_not_found(store):
    result = store.get_enrichment("1.2.3.4")
    assert result is None

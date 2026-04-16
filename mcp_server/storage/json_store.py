import json
from pathlib import Path
from typing import Any

import structlog

from .base import StorageBase

log = structlog.get_logger()


class JsonStore(StorageBase):
    def __init__(self, data_path: str | Path) -> None:
        self._path = Path(data_path)
        with self._path.open() as f:
            data = json.load(f)
        self._alerts: list[dict[str, Any]] = data.get("alerts", [])
        self._events: list[dict[str, Any]] = data.get("events", [])
        self._entity_context: dict[str, Any] = data.get("entity_context", {})
        self._ip_enrichment: dict[str, Any] = data.get("ip_enrichment", {})
        log.info("json_store.loaded", path=str(self._path), alerts=len(self._alerts))

    def get_alerts(self) -> list[dict[str, Any]]:
        return list(self._alerts)

    def get_alert(self, alert_id: str) -> dict[str, Any] | None:
        for alert in self._alerts:
            if alert.get("id") == alert_id:
                return dict(alert)
        return None

    def search_events(self, query: str) -> list[dict[str, Any]]:
        q = query.lower()
        return [
            dict(e)
            for e in self._events
            if q in json.dumps(e).lower()
        ]

    def get_entity_context(self, entity: str) -> dict[str, Any] | None:
        result = self._entity_context.get(entity)
        return dict(result) if result else None

    def get_enrichment(self, ip: str) -> dict[str, Any] | None:
        result = self._ip_enrichment.get(ip)
        return dict(result) if result else None

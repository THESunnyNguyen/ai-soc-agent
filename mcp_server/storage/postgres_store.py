from typing import Any

from .base import StorageBase


class PostgresStore(StorageBase):
    """PostgreSQL-backed store. Implemented in Phase 4."""

    def get_alerts(self) -> list[dict[str, Any]]:
        raise NotImplementedError("PostgresStore is not implemented until Phase 4")

    def get_alert(self, alert_id: str) -> dict[str, Any] | None:
        raise NotImplementedError("PostgresStore is not implemented until Phase 4")

    def search_events(self, query: str) -> list[dict[str, Any]]:
        raise NotImplementedError("PostgresStore is not implemented until Phase 4")

    def get_entity_context(self, entity: str) -> dict[str, Any] | None:
        raise NotImplementedError("PostgresStore is not implemented until Phase 4")

    def get_enrichment(self, ip: str) -> dict[str, Any] | None:
        raise NotImplementedError("PostgresStore is not implemented until Phase 4")

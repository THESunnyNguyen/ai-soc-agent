from abc import ABC, abstractmethod
from typing import Any


class StorageBase(ABC):
    @abstractmethod
    def get_alerts(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_alert(self, alert_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def search_events(self, query: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_entity_context(self, entity: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def get_enrichment(self, ip: str) -> dict[str, Any] | None:
        raise NotImplementedError

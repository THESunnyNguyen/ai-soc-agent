from typing import Any

import structlog
from pydantic import BaseModel, ValidationError

from mcp_server.storage.base import StorageBase

log = structlog.get_logger()


class SearchEventsInput(BaseModel):
    query: str


def search_events(store: StorageBase, query: str) -> list[dict[str, Any]]:
    try:
        params = SearchEventsInput(query=query)
    except ValidationError as e:
        log.warning("tool.search_events.invalid_input", error=str(e))
        return [{"error": str(e)}]

    results = store.search_events(params.query)
    log.info("tool.search_events", query=params.query, results=len(results))
    return results

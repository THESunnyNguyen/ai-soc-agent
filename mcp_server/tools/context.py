from typing import Any

import structlog
from pydantic import BaseModel, ValidationError

from mcp_server.storage.base import StorageBase

log = structlog.get_logger()


class GetEntityContextInput(BaseModel):
    entity: str


def get_entity_context(store: StorageBase, entity: str) -> dict[str, Any]:
    try:
        params = GetEntityContextInput(entity=entity)
    except ValidationError as e:
        log.warning("tool.get_entity_context.invalid_input", error=str(e))
        return {"error": str(e)}

    result = store.get_entity_context(params.entity)
    if result is None:
        log.info("tool.get_entity_context.not_found", entity=params.entity)
        return {"error": f"No context found for entity '{params.entity}'"}

    log.info("tool.get_entity_context", entity=params.entity)
    return result

from typing import Any

import structlog
from pydantic import BaseModel, ValidationError

from mcp_server.storage.base import StorageBase

log = structlog.get_logger()


class EnrichIpInput(BaseModel):
    ip: str


def enrich_ip(store: StorageBase, ip: str) -> dict[str, Any]:
    try:
        params = EnrichIpInput(ip=ip)
    except ValidationError as e:
        log.warning("tool.enrich_ip.invalid_input", error=str(e))
        return {"error": str(e)}

    result = store.get_enrichment(params.ip)
    if result is None:
        log.info("tool.enrich_ip.no_data", ip=params.ip)
        return {"ip": params.ip, "reputation_score": 0, "categories": [], "threat_feeds": [], "notes": "No enrichment data available"}

    log.info("tool.enrich_ip", ip=params.ip)
    return result

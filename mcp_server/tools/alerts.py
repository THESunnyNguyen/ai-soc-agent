from typing import Any

import structlog
from pydantic import BaseModel, ValidationError

from mcp_server.storage.base import StorageBase

log = structlog.get_logger()


class GetAlertInput(BaseModel):
    alert_id: str


def list_alerts(store: StorageBase) -> list[dict[str, Any]]:
    alerts = store.get_alerts()
    log.info("tool.list_alerts", count=len(alerts))
    return alerts


def get_alert(store: StorageBase, alert_id: str) -> dict[str, Any]:
    try:
        params = GetAlertInput(alert_id=alert_id)
    except ValidationError as e:
        log.warning("tool.get_alert.invalid_input", error=str(e))
        return {"error": str(e)}

    alert = store.get_alert(params.alert_id)
    if alert is None:
        log.info("tool.get_alert.not_found", alert_id=params.alert_id)
        return {"error": f"Alert '{params.alert_id}' not found"}

    log.info("tool.get_alert", alert_id=params.alert_id)
    return alert

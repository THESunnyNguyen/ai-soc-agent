from pathlib import Path
from typing import Any

import structlog
from pydantic import BaseModel, ValidationError

log = structlog.get_logger()

RUNBOOKS_DIR = Path(__file__).parent.parent.parent / "runbooks"


class GetRunbookInput(BaseModel):
    name: str


def get_runbook(name: str) -> dict[str, Any]:
    try:
        params = GetRunbookInput(name=name)
    except ValidationError as e:
        log.warning("tool.get_runbook.invalid_input", error=str(e))
        return {"error": str(e)}

    path = RUNBOOKS_DIR / f"{params.name}.md"
    if not path.exists():
        log.info("tool.get_runbook.not_found", name=params.name)
        return {"error": f"Runbook '{params.name}' not found"}

    content = path.read_text(encoding="utf-8")
    log.info("tool.get_runbook", name=params.name)
    return {"name": params.name, "content": content}

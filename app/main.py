from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class GenericPayload(BaseModel):
    id: str | None = None
    name: str | None = None
    cluster_id: str | None = None
    deployment_id: str | None = None
    alias: str | None = None
    status: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def service_payload(settings: Settings) -> dict[str, Any]:
    return {
        "service": settings.service_name,
        "role": settings.service_role,
        "title": settings.service_title,
        "description": settings.service_description,
        "split_enabled": settings.service_split_enabled,
        "updated_at": now_iso(),
    }


def payload_id(payload: GenericPayload | None) -> str:
    if payload and payload.id:
        return payload.id
    if payload and payload.name:
        return payload.name
    return str(uuid4())


settings = get_settings()
app = FastAPI(title=settings.service_title, version="0.1.0")
store: dict[str, dict[str, Any]] = {}


@app.get("/livez")
async def livez() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/service-info")
async def service_info() -> dict[str, Any]:
    return {
        **service_payload(settings),
        "service_to_service_urls": settings.service_to_service_urls,
    }


def row(resource: str, item_id: str, payload: GenericPayload | None = None, **extra: Any) -> dict[str, Any]:
    data = payload.model_dump(mode="json") if payload else {}
    status_value = data.get("status") or extra.pop("status", "accepted")
    item = {
        "id": item_id,
        "resource": resource,
        "service": settings.service_name,
        "role": settings.service_role,
        "status": status_value,
        "updated_at": now_iso(),
        **extra,
    }
    for key, value in data.items():
        if key != "status" and value is not None:
            item[key] = value
    store[f"{resource}:{item_id}"] = item
    return item


def list_rows(resource: str) -> list[dict[str, Any]]:
    return [value for key, value in sorted(store.items()) if key.startswith(f"{resource}:")]


@app.get("/costs/summary")
async def cost_summary() -> Any:
    return row("costs", "default", operation="cost_summary")


@app.get("/costs/history")
async def cost_history() -> Any:
    return row("costs", "default", operation="cost_history")


@app.get("/costs/model-rates")
async def list_model_rates() -> Any:
    return list_rows("costs")


@app.put("/costs/model-rates/{model_name:path}")
async def upsert_model_rate(model_name: str, payload: GenericPayload | None = None) -> Any:
    return row("costs", model_name, payload, operation="upsert_model_rate")


@app.get("/costs/electricity-price")
async def get_electricity_price() -> Any:
    return row("costs", "default", operation="get_electricity_price")


@app.put("/costs/electricity-price")
async def update_electricity_price(payload: GenericPayload | None = None) -> Any:
    return row("costs", payload_id(payload), payload, operation="update_electricity_price")


@app.post("/costs/usage-events")
async def record_cost_usage(payload: GenericPayload | None = None) -> Any:
    return row("costs", payload_id(payload), payload, operation="record_cost_usage")

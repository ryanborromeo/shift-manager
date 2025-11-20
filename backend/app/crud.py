from typing import Optional
from app.db import get_entity, put_entity, list_entities, get_entity_by_id, put_entity_with_auto_id, delete_entity, update_entity_by_id


DEFAULT_TIMEZONE = "UTC"


def get_timezone_setting() -> str:
    entity = get_entity("Settings", "timezone")
    if entity is None:
        return DEFAULT_TIMEZONE
    return entity.get("timezone", DEFAULT_TIMEZONE)


def update_timezone_setting(timezone: str) -> str:
    put_entity("Settings", "timezone", {"timezone": timezone})
    return timezone


def list_workers():
    entities = list_entities("Worker")
    return [{"id": entity.key.id, "name": entity["name"]} for entity in entities]


def create_worker(name: str):
    entity = put_entity_with_auto_id("Worker", {"name": name})
    return {"id": entity.key.id, "name": entity["name"]}


def get_worker(worker_id: int) -> Optional[dict]:
    entity = get_entity_by_id("Worker", worker_id)
    if entity is None:
        return None
    return {"id": entity.key.id, "name": entity["name"]}


def update_worker(worker_id: int, name: str) -> Optional[dict]:
    entity = update_entity_by_id("Worker", worker_id, {"name": name})
    if entity is None:
        return None
    return {"id": entity.key.id, "name": entity["name"]}


def delete_worker(worker_id: int) -> Optional[bool]:
    entity = get_entity_by_id("Worker", worker_id)
    if entity is None:
        return None
    delete_entity("Worker", worker_id)
    return True

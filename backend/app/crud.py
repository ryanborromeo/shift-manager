from datetime import datetime, timezone
from typing import Optional, List
from app.db import list_entities, get_entity_by_id, put_entity_with_auto_id, delete_entity, update_entity_by_id, list_entities_by_property


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


def to_utc(iso_string: str) -> datetime:
    dt = datetime.fromisoformat(iso_string)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def validate_worker_exists(worker_id: int) -> bool:
    entity = get_entity_by_id("Worker", worker_id)
    return entity is not None


def check_shift_overlap(worker_id: int, start_utc: datetime, end_utc: datetime, exclude_shift_id: Optional[int] = None) -> bool:
    shifts = list_entities_by_property("Shift", "worker_id", worker_id)
    for shift in shifts:
        if exclude_shift_id is not None and shift.key.id == exclude_shift_id:
            continue
        shift_start_utc = shift["start_utc"]
        shift_end_utc = shift["end_utc"]
        if (start_utc < shift_end_utc) and (shift_start_utc < end_utc):
            return True
    return False


def list_shifts() -> List[dict]:
    entities = list_entities("Shift")
    return [
        {
            "id": entity.key.id,
            "worker_id": entity["worker_id"],
            "start": entity["start_utc"].isoformat(),
            "end": entity["end_utc"].isoformat()
        }
        for entity in entities
    ]


def create_shift(worker_id: int, start: str, end: str) -> dict:
    if not validate_worker_exists(worker_id):
        raise ValueError("Worker not found")
    
    start_utc = to_utc(start)
    end_utc = to_utc(end)
    
    if check_shift_overlap(worker_id, start_utc, end_utc):
        raise ValueError("Shift overlaps with existing shift for this worker")
    
    entity = put_entity_with_auto_id("Shift", {
        "worker_id": worker_id,
        "start_utc": start_utc,
        "end_utc": end_utc
    })
    
    return {
        "id": entity.key.id,
        "worker_id": entity["worker_id"],
        "start": entity["start_utc"].isoformat(),
        "end": entity["end_utc"].isoformat()
    }


def get_shift(shift_id: int) -> Optional[dict]:
    entity = get_entity_by_id("Shift", shift_id)
    if entity is None:
        return None

    return {
        "id": entity.key.id,
        "worker_id": entity["worker_id"],
        "start": entity["start_utc"].isoformat(),
        "end": entity["end_utc"].isoformat()
    }


def update_shift(shift_id: int, worker_id: int, start: str, end: str) -> Optional[dict]:
    entity = get_entity_by_id("Shift", shift_id)
    if entity is None:
        return None
    
    if not validate_worker_exists(worker_id):
        raise ValueError("Worker not found")
    
    start_utc = to_utc(start)
    end_utc = to_utc(end)
    
    if check_shift_overlap(worker_id, start_utc, end_utc, exclude_shift_id=shift_id):
        raise ValueError("Shift overlaps with existing shift for this worker")
    
    updated_entity = update_entity_by_id("Shift", shift_id, {
        "worker_id": worker_id,
        "start_utc": start_utc,
        "end_utc": end_utc
    })
    
    if updated_entity is None:
        return None
    
    return {
        "id": updated_entity.key.id,
        "worker_id": updated_entity["worker_id"],
        "start": updated_entity["start_utc"].isoformat(),
        "end": updated_entity["end_utc"].isoformat()
    }


def delete_shift(shift_id: int) -> Optional[bool]:
    entity = get_entity_by_id("Shift", shift_id)
    if entity is None:
        return None
    delete_entity("Shift", shift_id)
    return True

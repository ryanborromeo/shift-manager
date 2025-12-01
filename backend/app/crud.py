from datetime import datetime, timezone
from typing import Optional, List
from zoneinfo import ZoneInfo, available_timezones
from app.db import list_entities, get_entity_by_id, put_entity_with_auto_id, delete_entity, update_entity_by_id, list_entities_by_property, get_entity, put_entity

DEFAULT_TIMEZONE = "Etc/UTC"

# Cache for available timezones (computed once at module load)
_available_timezones_cache: Optional[List[str]] = None


def get_available_timezones() -> List[str]:
    """Return sorted list of available IANA timezone identifiers."""
    global _available_timezones_cache
    if _available_timezones_cache is None:
        _available_timezones_cache = sorted(available_timezones())
    return _available_timezones_cache


def is_valid_timezone(tz: str) -> bool:
    """Check if a timezone identifier is valid."""
    return tz in get_available_timezones()


def get_timezone_info(tz: str) -> dict:
    """Build timezone metadata for a given IANA timezone identifier."""
    zone = ZoneInfo(tz)
    now = datetime.now(zone)
    
    # Get current offset
    utc_offset = now.utcoffset()
    offset_seconds = int(utc_offset.total_seconds()) if utc_offset else 0
    
    # Get standard offset (January 1st to avoid DST in most zones)
    jan_1 = datetime(now.year, 1, 1, 12, 0, 0, tzinfo=zone)
    std_offset = jan_1.utcoffset()
    std_offset_seconds = int(std_offset.total_seconds()) if std_offset else 0
    
    # Determine DST status
    dst = now.dst()
    has_dst = dst is not None and dst.total_seconds() != 0 or offset_seconds != std_offset_seconds
    is_dst_active = dst is not None and dst.total_seconds() > 0
    
    return {
        "timezone": tz,
        "currentLocalTime": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "currentUtcOffset": {
            "seconds": offset_seconds,
            "milliseconds": offset_seconds * 1000,
        },
        "standardUtcOffset": {
            "seconds": std_offset_seconds,
            "milliseconds": std_offset_seconds * 1000,
        },
        "hasDayLightSaving": has_dst,
        "isDayLightSavingActive": is_dst_active,
    }


def get_stored_timezone() -> str:
    """Retrieve the stored timezone from Datastore, defaulting to Etc/UTC."""
    entity = get_entity("Settings", "timezone")
    if entity is None:
        # Persist default and return
        put_entity("Settings", "timezone", {"value": DEFAULT_TIMEZONE})
        return DEFAULT_TIMEZONE
    return entity.get("value", DEFAULT_TIMEZONE)


def set_stored_timezone(tz: str) -> str:
    """Persist the selected timezone to Datastore."""
    put_entity("Settings", "timezone", {"value": tz})
    return tz


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


def localize_dt(dt_utc: datetime) -> str:
    """Convert a UTC datetime to the stored preferred timezone and return ISO string."""
    tz = ZoneInfo(get_stored_timezone())
    return dt_utc.astimezone(tz).isoformat()


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
            "start": localize_dt(entity["start_utc"]),
            "end": localize_dt(entity["end_utc"])
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
        "start": localize_dt(entity["start_utc"]),
        "end": localize_dt(entity["end_utc"])
    }


def get_shift(shift_id: int) -> Optional[dict]:
    entity = get_entity_by_id("Shift", shift_id)
    if entity is None:
        return None

    return {
        "id": entity.key.id,
        "worker_id": entity["worker_id"],
        "start": localize_dt(entity["start_utc"]),
        "end": localize_dt(entity["end_utc"])
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
        "start": localize_dt(updated_entity["start_utc"]),
        "end": localize_dt(updated_entity["end_utc"])
    }


def delete_shift(shift_id: int) -> Optional[bool]:
    entity = get_entity_by_id("Shift", shift_id)
    if entity is None:
        return None
    delete_entity("Shift", shift_id)
    return True

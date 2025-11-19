from app.db import get_entity, put_entity


DEFAULT_TIMEZONE = "UTC"


def get_timezone_setting() -> str:
    entity = get_entity("Settings", "timezone")
    if entity is None:
        return DEFAULT_TIMEZONE
    return entity.get("timezone", DEFAULT_TIMEZONE)


def update_timezone_setting(timezone: str) -> str:
    put_entity("Settings", "timezone", {"timezone": timezone})
    return timezone

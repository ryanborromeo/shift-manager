import os
from typing import Optional, List, Any
from google.cloud import datastore


_client = None


def get_client():
    global _client
    if _client is None:
        project_id = os.environ.get("DATASTORE_PROJECT_ID", "local-project")
        _client = datastore.Client(project=project_id)
    return _client


def get_entity(kind: str, key_name: str) -> Optional[Any]:
    client = get_client()
    key = client.key(kind, key_name)
    return client.get(key)


def put_entity(kind: str, key_name: str, data: dict) -> Any:
    client = get_client()
    key = client.key(kind, key_name)
    entity = datastore.Entity(key=key)
    entity.update(data)
    client.put(entity)
    return entity


def list_entities(kind: str) -> List[Any]:
    client = get_client()
    query = client.query(kind=kind)
    return list(query.fetch())


def delete_entity(kind: str, entity_id: int) -> None:
    client = get_client()
    key = client.key(kind, entity_id)
    client.delete(key)


def get_entity_by_id(kind: str, entity_id: int) -> Optional[Any]:
    client = get_client()
    key = client.key(kind, entity_id)
    return client.get(key)


def put_entity_with_auto_id(kind: str, data: dict) -> Any:
    client = get_client()
    key = client.key(kind)
    entity = datastore.Entity(key=key)
    entity.update(data)
    client.put(entity)
    return entity


def update_entity_by_id(kind: str, entity_id: int, data: dict) -> Optional[Any]:
    client = get_client()
    key = client.key(kind, entity_id)
    entity = client.get(key)
    if entity is None:
        return None
    entity.update(data)
    client.put(entity)
    return entity

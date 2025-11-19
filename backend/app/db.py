import os
from google.cloud import datastore


_client = None


def get_client():
    global _client
    if _client is None:
        project_id = os.environ.get("DATASTORE_PROJECT_ID", "local-project")
        _client = datastore.Client(project=project_id)
    return _client


def get_entity(kind: str, key_name: str):
    client = get_client()
    key = client.key(kind, key_name)
    return client.get(key)


def put_entity(kind: str, key_name: str, data: dict):
    client = get_client()
    key = client.key(kind, key_name)
    entity = datastore.Entity(key=key)
    entity.update(data)
    client.put(entity)
    return entity

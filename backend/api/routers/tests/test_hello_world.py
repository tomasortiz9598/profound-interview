from collections.abc import Generator
from datetime import datetime, timezone
from unittest.mock import MagicMock
import uuid

from api.dependencies import get_db
from api.main import app
from db.models.hello_world import HelloWorld
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_hello_world_returns_content() -> None:
    created_time = datetime(2026, 10, 22, tzinfo=timezone.utc)
    row_id = uuid.UUID("3f1c0a6e-7b24-4d8a-9c15-2e6b8a4d0f71")
    row = HelloWorld(
        id=row_id,
        content="Hello world",
        created_time=created_time,
        updated_time=created_time,
    )
    session = MagicMock(spec=Session)
    session.query.return_value.first.return_value = row

    def _override_db() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_db] = _override_db
    client = TestClient(app)
    try:
        response = client.get("/hello-world")
    finally:
        client.close()
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    assert response.json() == {
        "id": str(row_id),
        "content": "Hello world",
        "created_time": "2026-10-22T00:00:00Z",
        "updated_time": "2026-10-22T00:00:00Z",
    }

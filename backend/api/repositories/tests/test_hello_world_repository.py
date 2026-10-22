from datetime import datetime, timezone
from unittest.mock import MagicMock
import uuid

from api.repositories.hello_world_repository import HelloWorldRepository
from db.models.hello_world import HelloWorld


def test_get_hello_world_returns_seeded_row() -> None:
    created_time = datetime.now(timezone.utc)
    row = HelloWorld(
        id=uuid.uuid4(),
        content="Hello world",
        created_time=created_time,
        updated_time=created_time,
    )
    session = MagicMock()
    session.query.return_value.first.return_value = row

    repository = HelloWorldRepository(session=session)

    assert repository.get_hello_world() is row
    session.query.assert_called_once_with(HelloWorld)

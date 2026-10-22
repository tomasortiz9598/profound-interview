from collections.abc import Generator

from api.repositories.hello_world_repository import HelloWorldRepository
from db.session_creator import get_db_session
from fastapi import Depends
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    db = get_db_session(pool_size=10)
    try:
        yield db
    finally:
        db.close()


def get_hello_world_repository(
    session: Session = Depends(get_db),
) -> HelloWorldRepository:
    return HelloWorldRepository(session=session)

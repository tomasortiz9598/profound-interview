import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from utils.settings import AppSettings


def get_db_uri() -> str:
    _settings = AppSettings()
    return (
        f"postgresql+psycopg2://{_settings.PGUSER}:{_settings.PGPASSWORD}"
        f"@{_settings.PGHOST}:{_settings.PGPORT}/{_settings.PGDATABASE}"
    )


def get_db_session(
    postgres_url: str | None = None,
    echo: bool = False,
    pool_size: int | None = None,
    **kwargs: Any,
) -> Session:
    os.environ["SQLALCHEMY_WARN_20"] = "true"
    if postgres_url is None:
        postgres_url = get_db_uri()
    if pool_size:
        kwargs["pool_size"] = pool_size
        kwargs["max_overflow"] = 20
        kwargs["pool_recycle"] = 1800
        kwargs["pool_timeout"] = 30

    engine = create_engine(
        postgres_url, pool_pre_ping=True, future=True, echo=echo, **kwargs
    )
    session_maker = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )
    return session_maker()

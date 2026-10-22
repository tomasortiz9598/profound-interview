import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from db.models.base import Base
from db.models.hello_world import HelloWorld  # noqa: F401
from db.session_creator import get_db_uri

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _resolve_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    try:
        return get_db_uri()
    except Exception:
        db_host = os.getenv("DB_HOST", os.getenv("PGHOST", "localhost"))
        db_port = os.getenv("DB_PORT", os.getenv("PGPORT", "5432"))
        db_name = os.getenv("DB_NAME", os.getenv("PGDATABASE", "profound_interview"))
        db_user = os.getenv("DB_USER", os.getenv("PGUSER", "postgres"))
        db_password = os.getenv("DB_PASSWORD", os.getenv("PGPASSWORD", ""))
        if not any([db_host, db_name, db_user]):
            return context.config.get_main_option("sqlalchemy.url")

        if db_password:
            return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"


def run_migrations_offline() -> None:
    url = _resolve_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _resolve_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

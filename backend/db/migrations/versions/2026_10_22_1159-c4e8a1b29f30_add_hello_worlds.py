"""Add hello worlds

Revision ID: c4e8a1b29f30
Revises:
Create Date: 2026-10-22 11:59:00.000000

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c4e8a1b29f30"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))

    op.create_table(
        "hello_worlds",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "created_time",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_time",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.bulk_insert(
        sa.table(
            "hello_worlds",
            sa.column("id", postgresql.UUID(as_uuid=True)),
            sa.column("content", sa.String()),
        ),
        [
            {
                "id": uuid.UUID("3f1c0a6e-7b24-4d8a-9c15-2e6b8a4d0f71"),
                "content": "Hello world",
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("hello_worlds")

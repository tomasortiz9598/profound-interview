from db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column


class HelloWorld(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "hello_worlds"

    content: Mapped[str] = mapped_column(nullable=False)

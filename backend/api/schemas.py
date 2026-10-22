import datetime
import uuid

from pydantic import BaseModel


class HelloWorld(BaseModel):
    id: uuid.UUID
    content: str
    created_time: datetime.datetime
    updated_time: datetime.datetime

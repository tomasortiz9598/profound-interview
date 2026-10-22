from api.error_handlers import InvalidRequest
from db.models.hello_world import HelloWorld
from sqlalchemy.orm import Session


class HelloWorldRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_hello_world(self) -> HelloWorld:
        hello_world: HelloWorld | None = self.session.query(HelloWorld).first()
        if not hello_world:
            raise InvalidRequest("Hello world not found")
        return hello_world

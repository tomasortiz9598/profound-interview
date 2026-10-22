from api.dependencies import get_hello_world_repository
from api.repositories.hello_world_repository import HelloWorldRepository
from api.schemas import HelloWorld
from db.models.hello_world import HelloWorld as HelloWorldModel
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/hello-world", tags=["hello_world"])


@router.get("", response_model=HelloWorld)
async def get_hello_world(
    hello_world_repository: HelloWorldRepository = Depends(get_hello_world_repository),
) -> HelloWorld:
    hello_world: HelloWorldModel = hello_world_repository.get_hello_world()
    return HelloWorld(
        id=hello_world.id,
        content=hello_world.content,
        created_time=hello_world.created_time,
        updated_time=hello_world.updated_time,
    )

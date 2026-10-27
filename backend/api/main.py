from api.error_handlers import configure_exception_handlers, configure_middlewares
from api.routers.account_challenge_router import router as account_challenge_router
from api.routers.hello_world_router import router as hello_world_router
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()
    configure_middlewares(app)
    configure_exception_handlers(app)
    app.include_router(hello_world_router)
    app.include_router(account_challenge_router)
    return app


app = create_app()

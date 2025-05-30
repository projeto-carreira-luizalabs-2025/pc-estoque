import os

import dotenv
from fastapi import FastAPI

from app.container import Container
from app.settings import api_settings

ENV = os.getenv("ENV", "production")
is_dev = ENV == "dev"

dotenv.load_dotenv(override=is_dev)


def init() -> FastAPI:
    from app.api.api_application import create_app
    from app.api.router import routes as api_routes

    container = Container()

    container.config.from_pydantic(api_settings)

    app_api = create_app(api_settings, api_routes)
    app_api.container = container  # type: ignore[attr-defined]

    # Autowiring
    container.wire(modules=["app.api.common.routers.health_check_routers"])
    container.wire(modules=["app.api.v1.routers.estoque_router"])
    container.wire(modules=["app.api.v2.routers.estoque_router"])

    # Outros middlewares podem ser adicionados aqui se necessário

    return app_api


app = init()

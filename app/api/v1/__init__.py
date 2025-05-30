from fastapi import APIRouter

from app.settings import api_settings


router_estoque = APIRouter(prefix="/seller/v1", tags=["Estoque V1"])


def load_routes(router_estoque: APIRouter):
    if api_settings.enable_estoque_resources:
        from app.api.v1.routers.estoque_router import router

        router_estoque.include_router(router)


load_routes(router_estoque)

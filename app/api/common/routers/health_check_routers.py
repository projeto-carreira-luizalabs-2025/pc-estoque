from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI
from starlette import status

from app.container import Container

if TYPE_CHECKING:
    from app.settings import AppSettings


def add_health_check_router(app: FastAPI, prefix: str = "/api") -> None:
    health_router = APIRouter(prefix=prefix, tags=["Saúde da Aplicação"])

    @health_router.get(
        "/ping",
        operation_id="get_ping",
        name="Verificar acessibilidade da aplicação",
        description="Verifica se a aplicação está acessível",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    @health_router.head(
        "/ping",
        operation_id="head_ping",
        name="Verificar acessibilidade da aplicação",
        description="Verifica se a aplicação está acessível",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def ping():
        # XXX Verificar info da ....
        return

    @health_router.get(
        path="/health",
        summary="Health Check",
        include_in_schema=True,
        operation_id="get_health",
        name="Verificar saúde da aplicação",
        description="Verifica se a aplicação está operante bem como seus recursos",
        status_code=200,
    )
    @inject
    async def health_check(
        settings: "AppSettings" = Depends(Provide[Container.settings]),
    ):
        # XXX Fixado.
        return {"version": settings.version}

    app.include_router(health_router)

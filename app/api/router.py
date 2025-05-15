from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.api.v1 import estoque_api  # <-- importa o estoque_routes
from app.api.v1.estoque_api import estoque_routes
routes = APIRouter()

# Versão da API
VERSAO_API = "0.0.2"

# Modelo de resposta para o endpoint raiz
class RootResponse(BaseModel):
    versao: str = Field(
        VERSAO_API,
        description="Versão da API"
    )

@routes.get("/")
async def get_root():
    return {"message": "Bem vindo ao PC-Estoque"}

@routes.get("/api/health")
async def get_version() -> RootResponse:
    return RootResponse(versao=VERSAO_API)

# Inclui as rotas de estoque
routes.include_router(estoque_api.estoque_routes)
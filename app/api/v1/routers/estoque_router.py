from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.api.v1.schemas.estoque_schema import EstoqueCreate, EstoqueResponse, EstoqueUpdate
from app.services.estoque.estoque_service import EstoqueServices
from app.container import Container


router = APIRouter(prefix="/estoque", tags=["Estoque"])

@router.get(
    "",
    response_model=ListResponse[EstoqueResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque(
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    result = await estoque_service.list(paginator=paginator, filters={})
    return paginator.paginate(results=result)

@router.get(
    "/{seller_id}/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_by_seller_and_sku(
    seller_id: str,
    sku: str,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.find_by_seller_id_and_sku(seller_id, sku)

@router.post(
    "",
    response_model=EstoqueResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_estoque(
    estoque: EstoqueCreate,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    estoque_model = estoque.to_model()
    return await estoque_service.create(estoque_model)

@router.patch(
    "/{seller_id}/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject 
async def update_estoque_by_seller_and_sku(
    seller_id: str,
    sku: str,
    estoque_update: EstoqueUpdate,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.update(seller_id, sku, estoque_update)

@router.delete(
    "/{seller_id}/{sku}",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_estoque_by_seller_and_sku(
    seller_id: str,
    sku: str,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.delete(seller_id, sku)

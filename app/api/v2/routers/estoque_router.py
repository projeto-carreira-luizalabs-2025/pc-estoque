from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, status

from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.api.v2.schemas.estoque_schema import EstoqueCreateV2, EstoqueResponseV2, EstoqueUpdateV2
from app.services.estoque_service import EstoqueServices
from app.container import Container


router = APIRouter(prefix="/estoque", tags=["Estoque V2"])

@router.get(
    "",
    response_model=ListResponse[EstoqueResponseV2],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_v2(
    x_seller_id: str = Header(..., alias="x-seller-id"),
    quantity: int = None,
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    filters = {"seller_id": x_seller_id}
    if quantity is not None:
        filters["quantidade"] = quantity
    result = await estoque_service.list(paginator=paginator, filters=filters)
    return paginator.paginate(results=result)

@router.get(
    "/{sku}",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_by_seller_and_sku_v2(
    sku: str,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.find_by_seller_id_and_sku(x_seller_id, sku)

@router.post(
    "",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_estoque_v2(
    estoque: EstoqueCreateV2,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    estoque_model = estoque.to_model()
    estoque_model.seller_id = x_seller_id  # sobrescreve com valor do cabeçalho
    return await estoque_service.create(estoque_model)

@router.patch(
    "/{sku}",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_200_OK,
)
@inject 
async def update_estoque_by_seller_and_sku_v2(
    sku: str,
    estoque_update: EstoqueUpdateV2,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.update(x_seller_id, sku, estoque_update)

@router.delete(
    "/{sku}",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_estoque_by_seller_and_sku_v2(
    sku: str,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.delete(x_seller_id, sku)

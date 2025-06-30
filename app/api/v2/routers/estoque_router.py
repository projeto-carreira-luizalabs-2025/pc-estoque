from typing import Optional
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi import HTTPException

from app.api.common.dependencies import get_required_seller_id
from app.api.common.schemas import ListResponse, Paginator
from app.api.common.auth_handler import do_auth 
from app.api.common.schemas.pagination import get_request_pagination
from app.api.v2.schemas.estoque_schema import EstoqueCreateV2, EstoqueResponseV2, EstoqueUpdateV2
from app.models.estoque_model import Estoque
from app.services import EstoqueServices
from app.container import Container


router = APIRouter(prefix="/estoque", tags=["Estoque V2"], dependencies=[Depends(do_auth)])

@router.get(
    "",
    response_model=ListResponse[EstoqueResponseV2],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_v2(
    seller_id: str = Depends(get_required_seller_id),
    quantity: Optional[int] = None,  
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    filters = {"seller_id": seller_id}
    if quantity is not None:
        filters["quantidade"] = str(quantity)
    result = await estoque_service.list(paginator=paginator, filters=filters)
    return paginator.paginate(results=result)

@router.get(
    "/{sku}",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_200_OK,
    response_model_exclude_unset=True,  
)
@inject
async def list_estoque_by_seller_and_sku_v2(
    sku: str,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    if estoque_service is None:
        raise HTTPException(status_code=404, detail="Estoque service not found")
    estoque = await estoque_service.get_by_seller_id_and_sku(seller_id, sku)
    if estoque is None:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return estoque


@router.post(
    "",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_estoque_v2(
    estoque: EstoqueCreateV2,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    data = estoque.model_dump(exclude_unset=True)
    data["seller_id"] = seller_id
    estoque_model = Estoque(**data)
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
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    result = await estoque_service.update(seller_id, sku, estoque_update.quantidade)
    if result is None:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return result

@router.delete(
    "/{sku}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_estoque_by_seller_and_sku_v2(
    sku: str,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    result = await estoque_service.delete(seller_id, sku)
    if not result:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return None

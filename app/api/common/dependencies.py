from typing import Optional

from fastapi import Header

from app.api.common.schemas.response import ErrorDetail
from app.common.exceptions import BadRequestException


async def get_required_seller_id(
    seller_id: Optional[str] = Header(
        None, alias="x-seller-id", description="ID do vendedor obrigatório", convert_underscores=False
    )
) -> str:
    if seller_id is None:
        details = [
            ErrorDetail(
                message="Header 'seller-id' obrigatório",
                location="header",
                slug="missing_required_header",
                field="x-seller-id",
            )
        ]
        raise BadRequestException(details=details)
    return seller_id
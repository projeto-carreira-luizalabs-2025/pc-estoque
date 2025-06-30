from fastapi import HTTPException, status
from fastapi.requests import Request
from app.common.exceptions import BadRequestException


async def get_seller_id(request: Request) -> str:
    seller_id = request.headers.get("x-seller-id")
    if not seller_id:
        raise BadRequestException([{"message": "Seller ID não informado"}])

    return seller_id
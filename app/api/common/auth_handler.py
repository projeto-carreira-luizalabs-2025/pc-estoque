"""
'Camada' de segurança para a API
"""

from typing import TYPE_CHECKING, Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.common.injector import get_seller_id
from app.common.exceptions import ForbiddenException, UnauthorizedException
from app.container import Container
from app.integrations.auth.keycloak_adapter import OAuthException

if TYPE_CHECKING:
    from app.integrations.auth.keycloak_adapter import KeycloakAdapter

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8080/realms/marketplace/protocol/openid-connect/token"
)

@inject
async def do_auth(
    token: Annotated[str, Depends(oauth2_scheme)],
    seller_id: str = Depends(get_seller_id),
    openid_adapter: "KeycloakAdapter" = Depends(Provide[Container.keycloak_adapter]),
):
    """
    Responsável por fazer a autenticação com algum IDP OpenId.
    """

    try:
        info_token = await openid_adapter.validate_token(token)
    except OAuthException as exception:
        # XXX Poderíamos especializar as exceções
        raise UnauthorizedException from exception

    # Nossa autorização (permissão):
    # O usuário pode operar com o seller informado?
    if sellers := info_token.get("sellers", None):
        sellers = sellers.split(",")
    else:
        sellers = []

    if seller_id not in sellers:
        raise ForbiddenException([{"message": "não autorizado para trabalhar com este seller"}])
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import jwt
import httpx

from app.integrations.auth.keycloak_adapter import (
    KeycloakAdapter,
    InvalidTokenException,
    TokenExpiredException,
)

@pytest.fixture
def adapter():
    """Fixture que retorna uma instância do KeycloakAdapter com uma URL fake."""
    return KeycloakAdapter("https://fake-url.com/.well-known/openid-configuration")

def test_get_authorization_endpoint(adapter):
    """
    Testa se o método get_authorization_endpoint retorna o valor correto
    mockando o carregamento do well-known.
    """
    with patch.object(adapter, "_load_well_known") as mock_load:
        mock_load.return_value = {
            "authorization_endpoint": "https://example.com/auth"
        }
        result = adapter.get_authorization_endpoint()
        assert result == "https://example.com/auth"

@pytest.mark.asyncio
async def test_get_public_keys(adapter):
    """
    Testa se o método get_public_keys retorna as chaves públicas corretamente,
    mockando a resposta HTTP assíncrona com as chaves.
    """
    mock_keys = {"keys": [{"kid": "abc123", "kty": "RSA"}]}

    adapter._well_known = {"jwks_uri": "https://example.com/jwks"}

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_keys
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        keys = await adapter.get_public_keys()
        assert keys == mock_keys["keys"]

@pytest.mark.asyncio
async def test_get_alg_key_for_kid_found(adapter):
    """
    Testa se get_alg_key_for_kid retorna a chave correta quando o kid é encontrado.
    """
    adapter.get_public_keys = AsyncMock(return_value=[{"kid": "abc123", "alg": "RS256"}])
    key = await adapter.get_alg_key_for_kid("abc123")
    assert key["kid"] == "abc123"

@pytest.mark.asyncio
async def test_get_alg_key_for_kid_not_found(adapter):
    """
    Testa se get_alg_key_for_kid lança InvalidTokenException
    quando o kid não é encontrado.
    """
    adapter.get_public_keys = AsyncMock(return_value=[{"kid": "xyz"}])
    with pytest.raises(InvalidTokenException):
        await adapter.get_alg_key_for_kid("abc123")

@pytest.mark.asyncio
async def test_validate_token_success(adapter):
    """
    Testa o fluxo completo de validação de token com sucesso,
    mockando as chamadas internas e o decode do jwt.
    """
    token = "fake_token"
    kid = "kid123"
    alg = "RS256"
    fake_key = {"kid": kid, "kty": "RSA", "n": "fake_n", "e": "AQAB"}

    expected_info_token = {"sub": "user123", "iss": "issuer"}

    with patch.object(adapter, "get_header_info_from_token", return_value=(kid, alg)) as mock_get_header, \
         patch.object(adapter, "get_alg_key_for_kid", new=AsyncMock(return_value=fake_key)) as mock_get_key, \
         patch("jwt.PyJWK", return_value=MagicMock()) as mock_pyjwk, \
         patch("jwt.decode", return_value=expected_info_token) as mock_decode:

        result = await adapter.validate_token(token)

        mock_get_header.assert_called_once_with(token)
        mock_get_key.assert_awaited_once_with(kid)
        mock_pyjwk.assert_called_once_with(jwk_data=fake_key, algorithm=alg)
        mock_decode.assert_called_once()

        assert result == expected_info_token

@pytest.mark.asyncio
async def test_validate_token_invalid_key(adapter):
    """
    Testa se validate_token lança InvalidTokenException
    quando a chave do token não é encontrada.
    """
    token = "fake_token"
    kid = "invalid_kid"
    alg = "RS256"

    with patch.object(adapter, "get_header_info_from_token", return_value=(kid, alg)), \
         patch.object(adapter, "get_alg_key_for_kid", new=AsyncMock(side_effect=InvalidTokenException("Chave não encontrada"))):

        with pytest.raises(InvalidTokenException, match="Chave não encontrada"):
            await adapter.validate_token(token)

@pytest.mark.asyncio
async def test_validate_token_expired(adapter):
    """
    Testa se validate_token lança TokenExpiredException
    quando o token está expirado.
    """
    token = "fake_token"
    kid = "kid123"
    alg = "RS256"

    with patch.object(adapter, "get_header_info_from_token", return_value=(kid, alg)), \
         patch.object(adapter, "get_alg_key_for_kid", new=AsyncMock(side_effect=jwt.ExpiredSignatureError("Token expirou"))):

        with pytest.raises(TokenExpiredException, match="Token expirou"):
            await adapter.validate_token(token)

def test_load_well_known_success(adapter):
    """
    Testa o carregamento do well-known com sucesso,
    mockando resposta HTTP válida.
    """
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "authorization_endpoint": "https://example.com/auth",
        "jwks_uri": "https://example.com/jwks"
    }
    fake_response.raise_for_status = MagicMock()

    with patch("httpx.Client.get", return_value=fake_response) as mock_get:
        result = adapter._load_well_known()
        mock_get.assert_called_once_with(adapter.well_known_url, timeout=5)
        assert result["authorization_endpoint"] == "https://example.com/auth"
        assert result["jwks_uri"] == "https://example.com/jwks"

def test_load_well_known_http_error(adapter):
    """
    Testa tratamento de erro HTTP ao carregar well-known,
    simulando um erro HTTPStatusError.
    """
    fake_response = MagicMock()
    fake_response.status_code = 500
    fake_response.text = "Internal Server Error"
    http_error = httpx.HTTPStatusError(
        message="Error",
        request=MagicMock(),
        response=fake_response
    )

    with patch("httpx.Client.get", side_effect=http_error) as mock_get, \
         patch("builtins.print") as mock_print:
        result = adapter._load_well_known()
        mock_get.assert_called_once_with(adapter.well_known_url, timeout=5)
        mock_print.assert_called_with(f"Erro HTTP ao carregar well-known: 500 - Internal Server Error")
        assert result is None

def test_load_well_known_request_error(adapter):
    """
    Testa tratamento de erro de conexão ao carregar well-known,
    simulando um RequestError.
    """
    request_error = httpx.RequestError("Network failure", request=MagicMock())
    with patch("httpx.Client.get", side_effect=request_error) as mock_get, \
         patch("builtins.print") as mock_print:
        result = adapter._load_well_known()
        mock_get.assert_called_once_with(adapter.well_known_url, timeout=5)
        mock_print.assert_called_with("Erro de conexão ao carregar well-known: Network failure")
        assert result is None

def test_load_well_known_unexpected_error(adapter):
    """
    Testa tratamento de erro inesperado ao carregar well-known,
    simulando uma exceção genérica.
    """
    with patch("httpx.Client.get", side_effect=Exception("Unexpected")) as mock_get, \
         patch("builtins.print") as mock_print:
        result = adapter._load_well_known()
        mock_get.assert_called_once_with(adapter.well_known_url, timeout=5)
        mock_print.assert_called_with("Erro inesperado: Unexpected")
        assert result is None
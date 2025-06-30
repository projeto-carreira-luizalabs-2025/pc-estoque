from datetime import datetime
import pytest
from unittest.mock import AsyncMock
from httpx import ASGITransport, AsyncClient
from app.api.common.auth_handler import do_auth
from app.container import Container
from app.services import EstoqueServices
from app.models.estoque_model import Estoque
from app.common.datetime import utcnow

mock = AsyncMock(spec=EstoqueServices)
Container.estoque_service.override(mock)

from app.api_main import app 

# ----------------------------
# Fixtures
# ----------------------------

@pytest.fixture
def mock_estoque_service():
    yield mock
    Container.estoque_service.reset_override()

@pytest.fixture
def app_fixture():
    return app

@pytest.fixture
def mock_do_auth(app_fixture):
    app_fixture.dependency_overrides[do_auth] = lambda: None
    yield
    app_fixture.dependency_overrides.pop(do_auth, None)

@pytest.fixture
async def async_client(app_fixture):
    transport = ASGITransport(app=app_fixture)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000/seller/v2") as client:
        yield client

@pytest.fixture
def header_seller_id():
    return {"x-seller-id": "seller-123"}

@pytest.fixture
def now():
    """Fixture para retornar a data e hora atual."""
    return utcnow()

# ----------------------------
# Testes: GET /estoque
# ----------------------------

@pytest.mark.asyncio
async def test_listar_estoques(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Testa a listagem de estoques."""
    now = datetime.utcnow()
    mock_estoque_service.list.return_value = [
        Estoque(
            sku="ABC123",
            quantidade=10,
            seller_id="seller-123",
            updated_at=now,
            created_by="tester",
            updated_by="tester",
            audit_created_at=now,
            audit_updated_at=now,
            id=1
        ),
        Estoque(
            sku="DEF456",
            quantidade=5,
            seller_id="seller-123",
            updated_at=now,
            created_by="tester",
            updated_by="tester",
            audit_created_at=now,
            audit_updated_at=now,
            id=2
        ),
    ]

    resposta = await async_client.get("/estoque", headers=header_seller_id)

    assert resposta.status_code == 200
    data = resposta.json()
    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 2
    assert data["results"][0]["sku"] == "ABC123"
    assert data["results"][1]["sku"] == "DEF456"
    assert "meta" in data
    mock_estoque_service.list.assert_called_once()

@pytest.mark.asyncio
async def test_listar_estoques_sem_header(async_client):
    """Deve retornar erro se x-seller-id não for enviado."""
    resposta = await async_client.get("/estoque")
    assert resposta.status_code in (400, 401, 422)

@pytest.mark.asyncio
async def test_listar_estoques_com_quantity(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Testa a listagem de estoques com filtro de quantidade."""
    now = datetime.utcnow()
    mock_estoque_service.list.return_value = [
        Estoque(
            sku="ABC123",
            quantidade=5,
            seller_id="seller-123",
            updated_at=now,
            created_by="tester",
            updated_by="tester",
            audit_created_at=now,
            audit_updated_at=now,
            id=1
        ),
    ]
    resposta = await async_client.get("/estoque?quantity=5", headers=header_seller_id)
    assert resposta.status_code == 200
    data = resposta.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["quantidade"] == 5

# ----------------------------
# Testes: GET /estoque/{sku}
# ----------------------------

@pytest.mark.asyncio
async def test_buscar_estoque_por_sku(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Testa a busca de estoque por SKU."""
    sku = "ABC123"
    now = datetime.utcnow()
    mock_estoque_service.get_by_seller_id_and_sku.return_value = Estoque(
        sku=sku,
        quantidade=10,
        seller_id="seller-123",
        updated_at=now,
        created_by="tester",
        updated_by="tester",
        audit_created_at=now,
        audit_updated_at=now,
        id=None
    )

    resposta = await async_client.get(f"/estoque/{sku}", headers=header_seller_id)

    assert resposta.status_code == 200
    data = resposta.json()
    assert data["sku"] == sku
    assert data["quantidade"] == 10
    mock_estoque_service.get_by_seller_id_and_sku.assert_called_once_with("seller-123", sku)

@pytest.mark.asyncio
async def test_buscar_estoque_por_sku_inexistente(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Deve retornar 404 se o estoque não existir."""
    sku = "NAOEXISTE"
    mock_estoque_service.get_by_seller_id_and_sku.return_value = None

    resposta = await async_client.get(f"/estoque/{sku}", headers=header_seller_id)
    assert resposta.status_code == 404

@pytest.mark.asyncio
async def test_buscar_estoque_servico_none(async_client, mock_do_auth, header_seller_id, monkeypatch):
    """Deve retornar 404 se o estoque_service for None."""
    from app.api.v2.routers import estoque_router

    monkeypatch.setattr(
        estoque_router,
        "Container",
        type("FakeContainer", (), {"estoque_service": lambda: None})
    )
    resposta = await async_client.get("/estoque/ABC123", headers=header_seller_id)
    assert resposta.status_code == 404

# ----------------------------
# Testes: POST /estoque
# ----------------------------

@pytest.mark.asyncio
async def test_criar_estoque(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Testa a criação de um novo estoque."""
    payload = {
        "sku": "ABC123",
        "quantidade": 15
    }
    now = datetime.utcnow()
    mock_estoque_service.create.return_value = Estoque(
        sku=payload["sku"],
        quantidade=payload["quantidade"],
        seller_id="seller-123",
        updated_at=now,
        created_by="tester",
        updated_by="tester",
        audit_created_at=now,
        audit_updated_at=now,
        id=None
    )

    resposta = await async_client.post("/estoque", json=payload, headers=header_seller_id)

    assert resposta.status_code == 201
    data = resposta.json()
    assert data["sku"] == payload["sku"]
    assert data["quantidade"] == payload["quantidade"]
    mock_estoque_service.create.assert_called_once()

@pytest.mark.asyncio
async def test_criar_estoque_payload_invalido(async_client, mock_do_auth, header_seller_id):
    """Deve retornar 422 se payload for inválido."""
    payload = {"sku": "ABC123"}  # faltando 'quantidade'
    resposta = await async_client.post("/estoque", json=payload, headers=header_seller_id)
    assert resposta.status_code == 422

# ----------------------------
# Testes: PATCH /estoque/{sku}
# ----------------------------

@pytest.mark.asyncio
async def test_atualizar_estoque(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Testa a atualização de um estoque existente."""
    sku = "ABC123"
    nova_quantidade = 25
    now = datetime.utcnow()
    mock_estoque_service.update.return_value = Estoque(
        sku=sku,
        quantidade=nova_quantidade,
        seller_id="seller-123",
        updated_at=now,
        created_by="tester",
        updated_by="tester",
        audit_created_at=now,
        audit_updated_at=now,
        id=None
    )

    resposta = await async_client.patch(
        f"/estoque/{sku}",
        json={"quantidade": nova_quantidade},
        headers=header_seller_id
    )

    assert resposta.status_code == 200
    data = resposta.json()
    assert data["sku"] == sku
    assert data["quantidade"] == nova_quantidade
    mock_estoque_service.update.assert_called_once_with("seller-123", sku, nova_quantidade)

@pytest.mark.asyncio
async def test_atualizar_estoque_quantidade_invalida(async_client, mock_do_auth, header_seller_id):
    """Deve retornar 422 se quantidade for inválida."""
    sku = "ABC123"
    resposta = await async_client.patch(
        f"/estoque/{sku}",
        json={"quantidade": -10},  # quantidade negativa
        headers=header_seller_id
    )
    assert resposta.status_code == 422

@pytest.mark.asyncio
async def test_atualizar_estoque_inexistente(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Deve retornar 404 se tentar atualizar estoque inexistente."""
    sku = "NAOEXISTE"
    mock_estoque_service.update.return_value = None
    resposta = await async_client.patch(
        f"/estoque/{sku}",
        json={"quantidade": 10},
        headers=header_seller_id
    )
    assert resposta.status_code == 404

# ----------------------------
# Testes: DELETE /estoque/{sku}
# ----------------------------

@pytest.mark.asyncio
async def test_deletar_estoque(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Testa a exclusão de um estoque existente."""
    sku = "ABC123"

    mock_estoque_service.delete.return_value = True

    resposta = await async_client.delete(
        f"/estoque/{sku}",
        headers=header_seller_id
    )

    assert resposta.status_code == 204
    mock_estoque_service.delete.assert_called_once_with("seller-123", sku)

@pytest.mark.asyncio
async def test_deletar_estoque_inexistente(async_client, mock_estoque_service, mock_do_auth, header_seller_id):
    """Deve retornar 404 se tentar deletar estoque inexistente."""
    sku = "NAOEXISTE"
    mock_estoque_service.delete.return_value = None

    resposta = await async_client.delete(f"/estoque/{sku}", headers=header_seller_id)
    assert resposta.status_code == 404   
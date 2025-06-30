"""
Testes unitários para o SQLAlchemyCrudRepository.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, call
"""
Fixtures e utilitários auxiliares para os testes do SQLAlchemyCrudRepository.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.base.sqlalchemy_crud_repository import SQLAlchemyCrudRepository
from app.models.estoque_model import Estoque
from app.integrations.database.sqlalchemy_client import SQLAlchemyClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_session():
    """Retorna uma sessão assíncrona mockada."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_sqlalchemy_client(mock_session):
    """Retorna um cliente SQLAlchemy mockado, com a sessão simulada."""
    client = MagicMock(spec=SQLAlchemyClient)
    client.make_session.return_value.__aenter__.return_value = mock_session
    return client


@pytest.fixture
def estoque_model():
    """Instância Pydantic fictícia de Estoque."""
    return Estoque(id=1, seller_id="vendedor123", sku="sku123", quantidade=50)


@pytest.fixture
def estoque_base():
    """Entidade SQLAlchemy fictícia."""
    class EstoqueBase:
        id = None
        seller_id = None
        sku = None
        quantidade = None

    return EstoqueBase()


@pytest.fixture
def repository(mock_sqlalchemy_client, estoque_base):
    """Retorna uma instância de um repositório de teste derivado de SQLAlchemyCrudRepository."""
    class TestSQLAlchemyCrudRepository(SQLAlchemyCrudRepository):
        pass

    return TestSQLAlchemyCrudRepository(
        sql_client=mock_sqlalchemy_client,
        model_class=Estoque,
        entity_base_class=type(estoque_base)
    )

def test_to_base(repository, estoque_model):
    """Deve converter Estoque (Pydantic) para EstoqueBase (SQLAlchemy)."""
    result = repository.to_base(estoque_model)
    assert result.id == estoque_model.id


def test_to_model(repository, estoque_model, estoque_base, mock_sqlalchemy_client):
    """Deve converter EstoqueBase (SQLAlchemy) para Estoque (Pydantic)."""
    mock_sqlalchemy_client.to_dict.return_value = estoque_model.model_dump()
    result = repository.to_model(estoque_base)
    assert isinstance(result, type(estoque_model))


def test_to_model_returns_none_when_base_is_none(repository, mock_sqlalchemy_client):
    """Deve retornar None quando entidade base for None."""
    mock_sqlalchemy_client.to_dict.return_value = None
    assert repository.to_model(None) is None


@pytest.mark.asyncio
async def test_create(repository, mock_sqlalchemy_client, mock_session, estoque_model):
    """Deve criar um novo registro e retornar Estoque criado."""
    mock_sqlalchemy_client.to_dict.return_value = estoque_model.model_dump()
    result = await repository.create(estoque_model)
    mock_session.add.assert_called_once()
    assert isinstance(result, type(estoque_model))


@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku(repository, mock_sqlalchemy_client, mock_session, estoque_model, estoque_base):
    """Deve buscar Estoque pelo seller_id e sku."""
    repository._find_base_by_seller_id_sku_on_session = AsyncMock(return_value=estoque_base)
    repository.to_model = MagicMock(return_value=estoque_model)
    result = await repository.find_by_seller_id_and_sku("vendedor123", "sku123")
    assert result == estoque_model


@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_returns_none(repository):
    """Deve retornar None se registro não for encontrado."""
    repository._find_base_by_seller_id_sku_on_session = AsyncMock(return_value=None)
    repository.to_model = MagicMock(return_value=None)
    result = await repository.find_by_seller_id_and_sku("vendedor123", "sku123")
    assert result is None


def test_apply_sort(repository):
    """Deve aplicar ordenação conforme critérios de sort."""
    stmt_mock = MagicMock()
    stmt_mock.order_by.return_value = stmt_mock
    column_mock = MagicMock()
    repository.entity_base_class.id = column_mock
    repository.entity_base_class.name = column_mock
    sort_criteria = {"id": -1, "name": 1}
    result_stmt = repository._apply_sort(stmt_mock, sort_criteria)
    expected_calls = [call(column_mock.desc()), call(column_mock.asc())]
    stmt_mock.order_by.assert_has_calls(expected_calls)
    assert result_stmt == stmt_mock


@pytest.mark.asyncio
async def test_find_raises_type_error_with_invalid_filters(repository):
    """Deve levantar TypeError se os filtros forem inválidos."""
    with pytest.raises(TypeError):
        await repository.find(1234)


@pytest.mark.asyncio
async def test_delete_by_seller_id_and_sku(repository, mock_sqlalchemy_client, mock_session):
    """Deve deletar um registro e retornar True se deletou."""
    # Simula rowcount > 0 (deletou)
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_sqlalchemy_client.init_delete_estoque.return_value = MagicMock(where=MagicMock(return_value=MagicMock(where=MagicMock(return_value=MagicMock()))))
    result = await repository.delete_by_seller_id_and_sku("vendedor123", "sku123")
    assert result is True

@pytest.mark.asyncio
async def test_delete_by_seller_id_and_sku_not_found(repository, mock_sqlalchemy_client, mock_session):
    """Deve retornar False se não deletou nada."""
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result
    mock_sqlalchemy_client.init_delete_estoque.return_value = MagicMock(where=MagicMock(return_value=MagicMock(where=MagicMock(return_value=MagicMock()))))
    result = await repository.delete_by_seller_id_and_sku("vendedor123", "sku123")
    assert result is False

@pytest.mark.asyncio
async def test_update_by_seller_id_and_sku_success(repository, mock_sqlalchemy_client, mock_session, estoque_model, estoque_base):
    """Deve atualizar e retornar o modelo atualizado."""
    repository._find_base_by_seller_id_sku_on_session = AsyncMock(return_value=estoque_base)
    repository.to_model = MagicMock(return_value=estoque_model)
    mock_sqlalchemy_client.get_pk_fields.return_value = ["id"]
    mock_sqlalchemy_client.to_dict.return_value = estoque_model.model_dump()
    result = await repository.update_by_seller_id_and_sku("vendedor123", "sku123", estoque_model)
    assert result == estoque_model

@pytest.mark.asyncio
async def test_update_by_seller_id_and_sku_not_found(repository, mock_sqlalchemy_client, mock_session, estoque_model):
    """Deve retornar None se não encontrar para atualizar."""
    repository._find_base_by_seller_id_sku_on_session = AsyncMock(return_value=None)
    repository.to_model = MagicMock(return_value=None)
    result = await repository.update_by_seller_id_and_sku("vendedor123", "sku123", estoque_model)
    assert result is None

@pytest.mark.asyncio
async def test_patch_by_seller_id_and_sku_success(repository, mock_sqlalchemy_client, mock_session, estoque_base, estoque_model):
    """Deve atualizar parcialmente e retornar o modelo atualizado."""
    repository._find_base_by_seller_id_sku_on_session = AsyncMock(return_value=estoque_base)
    repository.to_model = MagicMock(return_value=estoque_model)
    patch_entity = MagicMock()
    patch_entity.model_dump.return_value = {"quantidade": 99}
    result = await repository.patch_by_seller_id_and_sku("vendedor123", "sku123", patch_entity)
    assert result == estoque_model

@pytest.mark.asyncio
async def test_patch_by_seller_id_and_sku_not_found(repository, mock_sqlalchemy_client, mock_session):
    """Deve retornar None se não encontrar para patch."""
    repository._find_base_by_seller_id_sku_on_session = AsyncMock(return_value=None)
    patch_entity = MagicMock()
    patch_entity.model_dump.return_value = {"quantidade": 99}
    result = await repository.patch_by_seller_id_and_sku("vendedor123", "sku123", patch_entity)
    assert result is None

@pytest.mark.asyncio
async def test_find_with_valid_filters(repository, mock_sqlalchemy_client, mock_session, estoque_base, estoque_model):
    """Deve buscar lista de entidades com filtros válidos."""
    mock_sqlalchemy_client.init_select_estoque.return_value = MagicMock(where=MagicMock(return_value=MagicMock()))
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [estoque_base]
    mock_session.execute.return_value = mock_result
    repository.to_model = MagicMock(return_value=estoque_model)
    filters = {"sku": "sku123"}
    result = await repository.find(filters)
    assert result == [estoque_model]
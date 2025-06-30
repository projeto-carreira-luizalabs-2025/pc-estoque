"""
Fixtures para testes de integração e unidade da API de Estoque.

Utiliza pytest para definir fixtures de container de dependências,
aplicação FastAPI, serviços, repositórios e mocks, além de dados de exemplo.
Permite isolar dependências e utilizar implementações mockadas durante os testes.
"""

from typing import Generator, List
from pytest import fixture
from fastapi import FastAPI

from app.container import Container
from app.models import Estoque
from app.repositories import EstoqueRepository
from app.services import HealthCheckService, EstoqueService
from app.settings import api_settings
from app.api.api_application import create_app
from app.api.router import router_configurations as api_routes
from dependency_injector import providers
from tests.factories.estoque_repository_factory_mocks import EstoqueRepositoryMockFactory


@fixture
def mock_estoque_repository() -> EstoqueRepository:
    """Retorna um repositório de estoque mockado para testes."""
    return EstoqueRepositoryMockFactory.create_mock_repository()


@fixture
def container(mock_estoque_repository: EstoqueRepository) -> Generator[Container, None, None]:
    """
    Cria e configura o container de dependências da aplicação para uso nos testes.
    Sobrescreve o repositório de estoque para utilizar uma implementação mockada.
    """
    container = Container()
    try:
        container.config.from_pydantic(api_settings)
        container.estoque_repository.override(providers.Object(mock_estoque_repository))
        yield container
    finally:
        container.unwire()


@fixture
def app(container: Container) -> Generator[FastAPI, None, None]:
    """
    Cria uma instância da aplicação FastAPI configurada para testes.
    Faz o wire do container com os módulos de rotas e health check.
    """
    import app.api.common.routers.health_check_routers as health_check_routers
    import app.api.v2.routers.estoque_router as estoque_router_v2

    container.wire(
        modules=[
            health_check_routers,
            estoque_router_v2,
        ]
    )

    app_instance = create_app(api_settings, api_routes)
    app_instance.container = container  # type: ignore[attr-defined]

    yield app_instance
    container.unwire()


@fixture
def estoque_repository(container: Container) -> EstoqueRepository:
    """Retorna a instância do repositório de estoque a partir do container configurado."""
    return container.estoque_repository()


@fixture
def estoque_service(container: Container) -> EstoqueService:
    """Retorna a instância do serviço de estoque a partir do container configurado."""
    return container.estoque_service()


@fixture
def health_check_service(container: Container) -> HealthCheckService:
    """Retorna a instância do serviço de health check a partir do container configurado."""
    return container.health_check_service()


@fixture
def test_estoques() -> List[Estoque]:
    """Gera e retorna uma lista de objetos de estoque para uso em testes unitários."""
    return [
        Estoque(
            seller_id="1",
            sku="A",
            quantidade=10,
            updated_at=None,
            created_by=None,
            updated_by=None,
            audit_created_at=None,
            audit_updated_at=None,
        ),
        Estoque(
            seller_id="2",
            sku="B",
            quantidade=20,
            updated_at=None,
            created_by=None,
            updated_by=None,
            audit_created_at=None,
            audit_updated_at=None,
        ),
    ]

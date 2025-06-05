from dependency_injector import containers, providers

from app.repositories import EstoqueRepository
from app.services import HealthCheckService
from app.services.estoque.estoque_service import EstoqueServices
from app.settings import AppSettings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Repositórios
    estoque_repository = providers.Singleton(EstoqueRepository)

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    estoque_service = providers.Singleton(EstoqueServices, repository=estoque_repository)

from dependency_injector import containers, providers

from app.repositories import EstoqueRepository
from app.services import HealthCheckService, EstoqueServices
from app.settings import AppSettings

from app.integrations.database.sqlalchemy_client import SQLAlchemyClient

from app.integrations.auth.keycloak_adapter import KeycloakAdapter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Integrações
    sql_client = providers.Singleton(SQLAlchemyClient, config.app_db_url)

    # Keycloak Adapter
    keycloak_adapter = providers.Singleton(KeycloakAdapter, config.app_openid_wellknown)

    # Repositórios
    estoque_repository = providers.Singleton(EstoqueRepository, sql_client=sql_client)

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    estoque_service = providers.Singleton(EstoqueServices, repository=estoque_repository)

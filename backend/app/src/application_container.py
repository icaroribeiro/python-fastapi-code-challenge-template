from dependency_injector import containers, providers
from src.infrastructure.repository.auth_repository import AuthRepository
from src.infrastructure.database.database_session_manager import DatabaseSessionManager
from src.service.auth_service import AuthService
from src.service.health_service import HealthService


async def session_factory(conn_string: str):
    database_session_manager = DatabaseSessionManager(conn_string=conn_string)
    async with database_session_manager.session() as session:
        yield session


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session = providers.Resource(session_factory, conn_string=config.db_conn_string)


class RepositoryContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    auth_repository = providers.Factory(AuthRepository, session=infrastructure.session)


class ServiceContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    repository = providers.DependenciesContainer()

    health_service = providers.Factory(HealthService, session=infrastructure.session)

    auth_service = providers.Factory(
        AuthService,
        auth_repository=repository.auth_repository_repository,
    )


class AppContainer(containers.DeclarativeContainer):
    config = Core.config

    infrastructure = providers.Container(InfrastructureContainer, config=config)

    repository = providers.Container(RepositoryContainer, infrastructure=infrastructure)

    service = providers.Container(
        ServiceContainer, infrastructure=infrastructure, repository=repository
    )

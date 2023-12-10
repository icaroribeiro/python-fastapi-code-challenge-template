from dependency_injector import containers, providers

from src.domain.repository.auth import AuthRepository
from src.infrastructure.database.database_session_manager import \
    DatabaseSessionManager
from src.service.auth import AuthService


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database_session_manager = providers.Factory(
        DatabaseSessionManager,
        conn_string=config.database_conn_string,
    )

    session_factory = providers.Factory(
        DatabaseSessionManager.session_factory,
        database_session_manager=database_session_manager,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    auth_repository = providers.Factory(
        AuthRepository, session=infrastructure.session_factory
    )


class ServiceContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    repository = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthService,
        jwt_auth=infrastructure.jwt_auth,
        auth_repository=repository.auth_repository,
    )


class AppContainer(containers.DeclarativeContainer):
    infrastructure = providers.Container(InfrastructureContainer, config=Core.config)

    repository = providers.Container(RepositoryContainer, infrastructure=infrastructure)

    service = providers.Container(
        ServiceContainer, infrastructure=infrastructure, repository=repository
    )

from dependency_injector import containers, providers

from src.domain.repository.auth import AuthRepository
from src.domain.repository.transaction import TransactionRepository
from src.infrastructure.database.database_session_manager import DatabaseSessionManager
from src.infrastructure.jwt.jwt_auth import JWTAuth
from src.service.auth import AuthService
from src.service.health import HealthService
from src.service.transaction import TransactionService


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

    jwt_auth = providers.Factory(JWTAuth)


class RepositoryContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    auth_repository = providers.Factory(
        AuthRepository, session=infrastructure.session_factory
    )

    transaction_repository = providers.Factory(
        TransactionRepository, session=infrastructure.session_factory
    )


class ServiceContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    repository = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthService,
        jwt_auth=infrastructure.jwt_auth,
        auth_repository=repository.auth_repository,
    )

    health_service = providers.Factory(
        HealthService, session=infrastructure.session_factory
    )

    transaction_service = providers.Factory(
        TransactionService,
        transaction_repository=repository.transaction_repository,
    )


class AppContainer(containers.DeclarativeContainer):
    infrastructure = providers.Container(InfrastructureContainer, config=Core.config)

    repository = providers.Container(RepositoryContainer, infrastructure=infrastructure)

    service = providers.Container(
        ServiceContainer, infrastructure=infrastructure, repository=repository
    )

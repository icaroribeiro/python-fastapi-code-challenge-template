from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.application_container import AppContainer, Core
from src.infrastructure.database import get_database_url
from src.router import auth_router as auth_router_module
from src.router import health_router as health_router_module
from src.router.auth_router import auth_router, auth_tag
from src.router.health_router import health_router, health_tag
from src.utils.api_exceptions import (
    ApiException,
    handle_api_exceptions,
    handle_request_validation_exception,
)


def create_app() -> FastAPI:
    database_url = get_database_url()
    Core.config.override({"database_url": database_url})

    container = AppContainer()
    container.wire(modules=[health_router_module])
    container.wire(modules=[auth_router_module])

    app = FastAPI(
        title="Code Challenge Template API",
        description="A REST API developed using **Python** programming language, **FastAPI** framework and **PostgreSQL** database.",
        version="1.0",
        openapi_tags=[health_tag, auth_tag],
        terms_of_service="http://swagger.io/terms/",
        contact={
            "name": "API Support",
            "email": "icaroribeiro@hotmail.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )
    app.include_router(router=health_router)
    app.include_router(router=auth_router)
    app.add_exception_handler(ApiException, handle_api_exceptions)
    app.add_exception_handler(
        RequestValidationError,
        handle_request_validation_exception,
    )
    return app

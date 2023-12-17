from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.application_container import AppContainer, Core
from src.controller.router import auth as auth_router_module
from src.controller.router.auth import auth_router, auth_tag
from src.infrastructure import application_settings
from src.infrastructure.database import build_db_conn_string
from src.utils.api_exceptions import (
    ApiException,
    handle_api_exceptions,
    handle_request_validation_exception,
)


def create_app() -> FastAPI:
    db_conn_string = build_db_conn_string()
    Core.config.override({"db_conn_string": db_conn_string})

    container = AppContainer()
    container.wire(modules=[auth_router_module])

    app = FastAPI(
        title="Code Challenge Template API",
        description="A REST API developed using **Python** programming language, **FastAPI** framework and **PostgreSQL** database.",
        version="1.0",
        openapi_tags=[auth_tag],
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
    app.include_router(router=auth_router)
    app.add_exception_handler(ApiException, handle_api_exceptions)
    app.add_exception_handler(
        RequestValidationError,
        handle_request_validation_exception,
    )
    return app

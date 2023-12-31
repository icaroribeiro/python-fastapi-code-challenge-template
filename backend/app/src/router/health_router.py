import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from src.application_container import AppContainer
from src.router.dto.health_response_dto import (
    HealthResponseDto,
    get_health_responses,
)
from src.service.health_service import HealthService
from src.utils.api_exceptions import ServerErrorException

logger = logging.getLogger(__name__)

health_tag = {
    "name": "health",
    "description": "Health check related operations",
}

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get(
    path="",
    responses=get_health_responses,
)
@inject
async def get_health(
    health_service: HealthService = Depends(
        Provide[AppContainer.service.health_service]
    ),
):
    try:
        await health_service.check_health()
    except Exception as ex:
        logger.error(f"Failed to check application's health: ${str(ex)}")
        raise ServerErrorException(
            extra="The application isn't ready to work as expected"
        )

    return HealthResponseDto(ok=True)

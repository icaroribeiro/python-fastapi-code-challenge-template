from fastapi import status
from pydantic import BaseModel
from src.controller.dto.error_dto import ErrorDto


class HealthResponseDto(BaseModel):
    ok: bool


get_health_responses = {
    status.HTTP_200_OK: {
        "model": HealthResponseDto,
        "description": "The application is healthy",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorDto,
    },
}

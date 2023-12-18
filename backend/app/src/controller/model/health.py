from fastapi import status
from pydantic import BaseModel

from src.controller.model.error import Error


class HealthResponse(BaseModel):
    ok: bool


get_health_responses = {
    status.HTTP_200_OK: {
        "model": HealthResponse,
        "description": "The application is healthy",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}

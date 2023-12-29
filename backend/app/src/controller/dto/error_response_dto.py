from pydantic import BaseModel


class ErrorResponseDto(BaseModel):
    message: str
    extra: str

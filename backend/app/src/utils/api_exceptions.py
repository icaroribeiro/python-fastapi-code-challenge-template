from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiException(HTTPException):
    def __init__(self, message: str, extra: str, status_code: int):
        super().__init__(status_code)
        self.message = message
        self.extra = extra
        self.status_code = status_code

    def to_dict(self):
        rv = {"message": self.message}
        if self.extra:
            rv["extra"] = self.extra
        return rv


class NoContentException(ApiException):
    def __init__(
        self,
        message=None,
        extra=None,
        status_code: int = status.HTTP_204_NO_CONTENT,
    ):
        super().__init__(message=message, extra=extra, status_code=status_code)


class BadRequestException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Bad request",
        extra=None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message=message, extra=extra, status_code=status_code)


class UnauthorizedException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Unauthorized access",
        extra=None,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message=message, extra=extra, status_code=status_code)


class ForbiddenException(ApiException):
    def __init__(
        self,
        message: str = "Oops! You don't have enough privileges to perform an action on this resource",
        extra=None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        super().__init__(message=message, extra=extra, status_code=status_code)


class RequestEntityTooLargeException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Request entity is too large",
        extra=None,
        status_code: int = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    ):
        super().__init__(message=message, extra=extra, status_code=status_code)


class InvalidFileFormatException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Invalid file format",
        extra=None,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        super().__init__(message=message, extra=extra, status_code=status_code)


class ServerErrorException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Something went wrong",
        extra: str = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(extra=extra, message=message, status_code=status_code)


def handle_api_exceptions(request: Request, ex: ApiException):
    return JSONResponse(status_code=ex.status_code, content=ex.to_dict())


def handle_request_validation_exception(request: Request, ex: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "message": "Request validation error",
                "extra": ex.errors()[0]["msg"],
            }
        ),
    )

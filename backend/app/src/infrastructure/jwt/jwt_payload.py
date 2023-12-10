from uuid import uuid4

from pydantic import BaseModel


class JWTPayload(BaseModel):
    jti: str
    auth_id: str
    login_id: str
    iat: int
    exp: int
    iss: str = "app"

from src.domain.model.auth import Auth
from src.domain.repository.auth import AuthRepository


class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
    ):
        self.__auth_repository = auth_repository

    async def save_auth(self, auth: Auth) -> Auth:
        return await self.__auth_repository.create_auth(auth=auth)

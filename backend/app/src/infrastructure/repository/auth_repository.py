from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.model.auth import Auth


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_auth(self, auth: Auth) -> Auth:
        try:
            self.__session.add(auth)
            await self.__session.commit()
            await self.__session.refresh(auth)
            return auth
        except Exception:
            await self.__session.rollback()
            raise

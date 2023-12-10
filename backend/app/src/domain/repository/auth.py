from src.domain.model.auth import Auth


class AuthRepository:
    def __init__(self, session):
        self.__session = session

    async def create_auth(self, auth: Auth) -> Auth:
        async with self.__session() as session:
            session.add(auth)
            await session.commit()
            await session.refresh(auth)
            return auth

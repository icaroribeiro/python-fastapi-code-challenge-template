from datetime import datetime
from typing import Optional

from fastapi.logger import logger
from sqlalchemy import and_, insert, select, update

from src.domain.model.auth import Auth
from src.utils.api_exceptions import ServerErrorException


class AuthRepository:
    def __init__(self, session):
        self.__session = session

    async def create_auth(self, auth: Auth) -> Auth:
        async with self.__session() as session:
            session.add(auth)
            await session.commit()
            await session.refresh(auth)

            return auth

    # async def get_auth_by_id(self, id: str) -> Optional[Auth]:
    #     async with self.session() as session:
    #         select_statement = select(Auth).where(Auth.id == id)
    #
    #         result = await session.execute(statement=select_statement)
    #
    #         auth = result.scalar()
    #
    #         if not auth:
    #             return None
    #
    #         return auth
    #
    # async def get_auth_by_username(self, username: str) -> Optional[Auth]:
    #     async with self.session() as session:
    #         select_statement = select(Auth).where(Auth.username == username)
    #
    #         result = await session.execute(statement=select_statement)
    #
    #         auth = result.scalar()
    #
    #         if not auth:
    #             return None
    #
    #         return auth
    #
    # async def update_auth(self, auth: Auth) -> Optional[Auth]:
    #     async with self.session() as session:
    #         update_statement = (
    #             update(Auth)
    #             .returning(Auth)
    #             .where(Auth.id == auth.id)
    #             .values(
    #                 username=auth.username,
    #                 password=auth.password,
    #                 login_id=auth.login_id,
    #                 refresh_token_id=auth.refresh_token_id,
    #                 updated_at=datetime.now(),
    #             )
    #         )
    #
    #         result = await session.execute(statement=update_statement)
    #
    #         auth = result.scalar()
    #
    #         if not auth:
    #             return None
    #
    #         await session.commit()
    #
    #         return auth
    #
    # async def update_auth_refresh_token_id(
    #     self, id: str, old_refresh_token_id: str, new_refresh_token_id: str
    # ) -> Optional[Auth]:
    #     async with self.session() as session:
    #         update_statement = (
    #             update(Auth)
    #             .returning(Auth)
    #             .where(
    #                 and_(
    #                     Auth.id == id,
    #                     Auth.refresh_token_id == old_refresh_token_id,
    #                 )
    #             )
    #             .values(refresh_token_id=new_refresh_token_id)
    #         )
    #
    #         result = await session.execute(statement=update_statement)
    #
    #         auth = result.scalar()
    #
    #         if not auth:
    #             return None
    #
    #         await session.commit()
    #
    #         return auth

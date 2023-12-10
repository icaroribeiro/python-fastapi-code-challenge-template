from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)


class DatabaseSessionManager:
    def __init__(self, conn_string: str):
        self.__engine = create_async_engine(url=conn_string)
        self.__sessionmaker = async_sessionmaker(autocommit=False, bind=self.__engine)

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    async def close(self):
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        await self.__engine.dispose()

        self.__engine = None
        self.__sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.__sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.__sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @staticmethod
    def session_factory(database_session_manager: "DatabaseSessionManager"):
        return database_session_manager.session

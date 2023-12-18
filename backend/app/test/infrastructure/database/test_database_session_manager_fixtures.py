import pytest
from sqlalchemy import delete

from src import build_db_conn_string
from src.infrastructure.database import Base
from src.infrastructure.database.database_session_manager import DatabaseSessionManager


class TestDatabaseSessionManagerFixtures:
    @pytest.fixture
    async def database_session_manager(self):
        conn_string = build_db_conn_string()
        database_session_manager = DatabaseSessionManager(conn_string=conn_string)
        yield database_session_manager
        async with database_session_manager.connect() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                await connection.execute(delete(table))
        await database_session_manager.close()

    @pytest.fixture
    async def session(self, database_session_manager: DatabaseSessionManager):
        async with database_session_manager.session() as session:
            yield session

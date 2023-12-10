import pytest
from sqlalchemy import delete
from src import build_database_conn_string
from src.infrastructure.database import Base
from src.infrastructure.database.database_session_manager import DatabaseSessionManager


class TestDatabaseSessionManagerFixtures:
    @pytest.fixture(scope="session", autouse=True)
    async def sessionmanager(self, event_loop):
        conn_string = build_database_conn_string()
        sessionmanager = DatabaseSessionManager(conn_string=conn_string)
        yield sessionmanager
        await sessionmanager.close()

    @pytest.fixture(scope="function", autouse=True)
    async def session(self, sessionmanager: DatabaseSessionManager):
        async with sessionmanager.session() as session:
            yield session

    @pytest.fixture(scope="function", autouse=True)
    async def clear_tables(self, sessionmanager: DatabaseSessionManager):
        async with sessionmanager.connect() as connection:
            tables = self._select_tables_to_delete()
            for table in tables:
                await connection.execute(delete(table))

    @staticmethod
    def _select_tables_to_delete():
        tables = [table for table in reversed(Base.metadata.sorted_tables)]
        tables.remove(SalespersonTransactionType.__table__)
        tables.remove(TransactionType.__table__)
        return tables

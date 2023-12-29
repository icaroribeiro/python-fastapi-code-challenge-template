from sqlalchemy import Result, text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthService:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def check_health(self) -> Result:
        return await self.__session.execute(statement=text("""SELECT 1"""))

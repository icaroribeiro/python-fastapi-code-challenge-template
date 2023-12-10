from sqlalchemy import Result, text


class HealthService:
    def __init__(self, session):
        self.session = session

    async def check_health(self) -> Result:
        async with self.session() as session:
            statement = text("""SELECT 1""")
            return await session.execute(statement=statement)

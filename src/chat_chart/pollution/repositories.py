from abc import ABC, abstractmethod

from sqlalchemy import text

from chat_chart.managers.database_manager import DatabaseManager
from chat_chart.pollution.entities import ResultTable


class PollutionRepository(ABC):
    @abstractmethod
    async def run_sql(self, sql: str) -> ResultTable:
        pass


class SQLAlchemyPollutionRepository(PollutionRepository):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def run_sql(self, sql: str) -> ResultTable:
        session = self._database_manager.get_session()
        async with session:
            statement = text(sql)
            rows = (await session.execute(statement=statement)).all()

        if len(rows) == 0:
            return ResultTable(
                headers=[],
                rows=[],
            )

        return ResultTable(
            headers=list(rows[0]._fields),
            rows=[list(row._data) for row in rows],
        )

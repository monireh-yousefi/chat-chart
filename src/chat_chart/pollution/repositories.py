from abc import ABC, abstractmethod

from sqlalchemy import select, text

from chat_chart.managers.database_manager import DatabaseManager
from chat_chart.pollution.entities import ResultTable
from chat_chart.pollution.orm import PollutionSubmissionORM


class PollutionRepository(ABC):
    @abstractmethod
    async def get_pollution_submissions(self, sql_query: str) -> ResultTable:
        pass


class SQLAlchemyPollutionRepository(PollutionRepository):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def get_pollution_submissions(self, sql_query: str) -> ResultTable:
        session = self._database_manager.get_session()
        async with session:
            textual_query = text(sql_query).columns(
                PollutionSubmissionORM.region,
                PollutionSubmissionORM.iso3,
                PollutionSubmissionORM.country,
                PollutionSubmissionORM.city,
                PollutionSubmissionORM.year,
                PollutionSubmissionORM.pm25,
                PollutionSubmissionORM.pm10,
                PollutionSubmissionORM.no2,
            )
            statement = select(PollutionSubmissionORM).from_statement(text(sql_query))
            orm_models = await session.scalars(statement)

        # TODO: execute doesn't return ORM models.
        return [orm_model.to_entity() for orm_model in orm_models.all()]

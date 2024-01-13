from chat_chart.llm.entities import LLMMessage, LLMMessageRole
from chat_chart.llm.services import LLMService
from chat_chart.pollution.entities import ResultTable
from chat_chart.pollution.repositories import PollutionRepository


class PollutionService:
    def __init__(
            self,
            llm_service: LLMService,
            pollution_repository: PollutionRepository,
    ):
        self._llm_service = llm_service
        self._pollution_repository = pollution_repository

    async def get_query_table(self, message: str) -> ResultTable:
        sql_query = await self._llm_service.query(
            messages=[
                LLMMessage(
                    role=LLMMessageRole.SYSTEM,
                    content='You are a SQL query generator for pollution submissions table.\n' \
                            'The query should consist of a single SELECT statement.\n' \
                            'The table name is `pollution_submissions` and it contains amount of pollution through different years and different cities.\n' \
                            'The table contains the following fields:\n' \
                            '"region": A text field containing the region of submission.\n' \
                            '"iso3": A text field containing ISO3 code of the country.\n' \
                            '"country": A text field containing the country of submission.\n' \
                            '"city": A text field containing the city of submission.\n' \
                            '"year": A integer field containing the year of submission.\n' \
                            '"pm25": Float field containing amount of PM2.5 which is particle pollution from fine particulates.\n' \
                            '"pm10": Float field containing amount of particles with a diameter of 10 micrometers or less.\n' \
                            '"no2": Float field containing amount of nitrogen in the air.'
                ),
                LLMMessage(
                    role=LLMMessageRole.USER,
                    content=f'Generate a SQL query to answer the following message:\n {message}'
                ),
            ]
        )

        return await self._pollution_repository.get_pollution_submissions(
            sql_query=sql_query,
        )

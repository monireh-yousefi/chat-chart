from __future__ import annotations

from functools import cached_property

from chat_chart.base.api_router import router as base_router
from chat_chart.config import AppConfig
from chat_chart.llm.services import LLMService, OpenAILLMService
from chat_chart.managers.api_manager import APIManager
from chat_chart.managers.database_manager import DatabaseManager
from chat_chart.pollution.api_router import router as pollution_router
from chat_chart.pollution.repositories import PollutionRepository, SQLAlchemyPollutionRepository
from chat_chart.pollution.services import PollutionService


class AppContainer:
    _INSTANCE: AppContainer | None = None

    @classmethod
    def get_instance(cls) -> AppContainer:
        if not cls._INSTANCE:
            cls._INSTANCE = AppContainer()

        return cls._INSTANCE

    @cached_property
    def config(self) -> AppConfig:
        return AppConfig()

    @cached_property
    def api_manager(self) -> APIManager:
        return APIManager(
            debug=self.config.debug,
            host=self.config.api_host,
            port=self.config.api_port,
            title=self.config.api_title,
            version=self.config.api_version,
            project_path=self.config.project_path,
            container=self,
            routers=[
                base_router,
                pollution_router,
            ],
        )

    @cached_property
    def database_manager(self) -> DatabaseManager:
        return DatabaseManager(
            debug=self.config.debug,
            database_uri=self.config.database_uri,
        )

    @cached_property
    def pollution_repository(self) -> PollutionRepository:
        return SQLAlchemyPollutionRepository(
            database_manager=self.database_manager,
        )

    @cached_property
    def llm_service(self) -> LLMService:
        return OpenAILLMService(
            api_key=self.config.openai_api_key,
            model_name=self.config.openai_model_name,
        )

    @cached_property
    def pollution_service(self) -> PollutionService:
        return PollutionService(
            llm_service=self.llm_service,
            pollution_repository=self.pollution_repository,
        )

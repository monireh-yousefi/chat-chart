from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='chat_pollution_',
        case_sensitive=False,
    )

    debug: bool = False

    api_host: str = "0.0.0.0"
    api_port: int = 8080
    api_title: str = "Chat Chart"
    api_version: str = "1.0.0"

    database_uri: str = 'sqlite+aiosqlite:///../database.sqlite'

    openai_api_key: str
    openai_model_name: str = "gpt-3.5-turbo"

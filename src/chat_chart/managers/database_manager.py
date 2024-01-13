from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class DatabaseManager:
    def __init__(
            self,
            debug: bool,
            database_uri: str,
    ):
        self._engine = create_async_engine(
            url=database_uri,
            echo=debug,
        )
        self._session_maker = async_sessionmaker(bind=self._engine)

    def get_session(self) -> AsyncSession:
        return self._session_maker()

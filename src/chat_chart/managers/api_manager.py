from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI, APIRouter

if TYPE_CHECKING:
    from chat_chart.container import AppContainer


class APIManager:
    def __init__(
            self,
            debug: bool,
            host: str,
            port: int,
            title: str,
            version: str,
            container: "AppContainer",
            routers: list[APIRouter],
    ):
        self._app = FastAPI(
            debug=debug,
            title=title,
            version=version,
        )
        for router in routers:
            self._app.include_router(router)
        self._app.state.container = container

        self._server = uvicorn.Server(
            uvicorn.Config(
                app=self._app,
                host=host,
                port=port,
            )
        )

    async def start(self) -> None:
        await self._server.serve()

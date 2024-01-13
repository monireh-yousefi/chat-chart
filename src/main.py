import asyncio

from chat_chart.container import AppContainer


async def main() -> None:
    await AppContainer.get_instance().api_manager.start()


if __name__ == '__main__':
    asyncio.run(main())

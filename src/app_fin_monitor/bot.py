import asyncio
import logging

from config_reader import config

from handlers import callback_hadler
from handlers import message_handler
from aiogram import Bot, Dispatcher
from middleware.repo_middleware import RepositoryMiddleware
from middleware.db_middleware import DataBaseSession
from middleware.access_chek_middleware import AccessChekMiddleware

from adapters.repository import SQLAlchemyRepository

from db.db_contrrol import create_all_db, drop_all_db, sessionmaker


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
    "%(lineno)d - %(name)s - %(message)s",
)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_all_db()

    await create_all_db()


async def on_shutdown(bot):
    print("бот лег")


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.workflow_data["_id_owner"] = int(config.id_owner.get_secret_value())
    dp.include_router(message_handler.router)
    dp.include_router(callback_hadler.router)
    dp.update.outer_middleware(AccessChekMiddleware())
    dp.update.middleware(DataBaseSession(session_pool=sessionmaker))
    dp.update.middleware(RepositoryMiddleware(SQLAlchemyRepository))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

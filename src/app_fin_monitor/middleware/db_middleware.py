import logging
from typing import Any, Callable, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

logger = logging.getLogger(__name__)


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        hadler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.debug(
            "Вошли в миддлварь %s, тип события %s",
            __class__.__name__,
            event.__class__.__name__,
        )
        async with self.session_pool() as session:
            data["session"] = session
            logger.debug("Выходим из миддлвари  %s", __class__.__name__)
            return await hadler(event, data)

import logging
from typing import Any, Callable, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from adapters.repository import SQLAlchemyRepository

logger = logging.getLogger(__name__)


class RepositoryMiddleware(BaseMiddleware):
    def __init__(self, repo: SQLAlchemyRepository):
        self.repo = repo

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
        data["repo"] = self.repo(data["session"])
        logger.debug("Выходим из миддлвари  %s", __class__.__name__)
        return await hadler(event, data)

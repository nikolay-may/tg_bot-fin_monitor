import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)

class AccessChekMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str,Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        user: User = data.get('event_from_user')
        id_owner = data.get('_id_owner')

        if user is not None and user.id  == id_owner:

            return await handler(event, data)
        else:
            logger.debug('Выходим из миддлвари  %s', __class__.__name__)
            return

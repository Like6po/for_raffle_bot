from typing import Callable, Dict, Any, Awaitable

from aiogram.types import CallbackQuery

from middlewares.database_upd.base import DatabaseUpdMiddleware


class OnChannelCbqDBUpd(DatabaseUpdMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       cbq: CallbackQuery,
                       data: Dict[str, Any]):
        if not super()._check_user_actuality(cbq.from_user, data["user_data"]):
            await data["user_db"].set(user=cbq.from_user)
        await handler(cbq, data)

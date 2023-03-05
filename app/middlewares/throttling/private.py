from typing import Callable, Dict, Any, Awaitable

from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache

from middlewares.throttling.base import ThrottlingMiddleware

THROTTLE_TEXT = "⛔ От вас идет слишком много запросов, пожалуйста, не так быстро!"


async def throttle(obj: Message | CallbackQuery,
                   cache: TTLCache):
    full_key = f"{obj.from_user.id}"

    if full_key not in cache:
        cache[full_key] = 3
        return

    cache[full_key] -= 1

    if cache[full_key] == 0:  # Оповещение + игнорирование
        return True
    elif cache[full_key] <= -1:  # Игнорирование
        return False


class ThrottlingPrivateMsgMiddleware(ThrottlingMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       obj: Message,
                       data: Dict[str, Any]):
        if (result := await throttle(obj=obj, cache=self.cache_msg)) is True:
            return await obj.reply(THROTTLE_TEXT)
        elif result is False:
            return
        await handler(obj, data)


class ThrottlingPrivateCbqMiddleware(ThrottlingMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       cbq: CallbackQuery,
                       data: Dict[str, Any]):
        if (result := await throttle(obj=cbq, cache=self.cache_cbq)) is True:
            return await cbq.answer(THROTTLE_TEXT, show_alert=True)
        elif result is False:
            return
        await handler(cbq, data)

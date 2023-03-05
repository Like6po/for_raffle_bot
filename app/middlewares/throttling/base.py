from abc import abstractmethod
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.cache_msg = TTLCache(maxsize=1000, ttl=2)
        self.cache_cbq = TTLCache(maxsize=1000, ttl=1)
        super().__init__()

    @abstractmethod
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       obj: TelegramObject,
                       data: Dict[str, Any]):
        await handler(obj, data)

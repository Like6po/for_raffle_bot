from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types.user import User as AiogramUser

from database.models import User


class DatabaseUpdMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       obj: TelegramObject,
                       data: Dict[str, Any]):
        await handler(obj, data)

    @classmethod
    def _check_user_actuality(cls, user: AiogramUser, data_user: User):
        if user.username != data_user.username:
            return False
        if user.full_name != data_user.full_name:
            return False
        return True

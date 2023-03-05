from typing import Dict, Any, Callable, Awaitable

from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares.database_init.base import DatabaseInitMiddleware


class OnPrivateMsgDBInit(DatabaseInitMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       message: Message,
                       data: Dict[str, Any]):
        session: AsyncSession = self.session_pool()
        data["session"] = session
        data["bot_pickle"] = self.bot_pickle
        data["scheduler"] = self.scheduler

        super().create_contexts(data, session)

        await super().set_user_to_contexts(data, message.from_user)

        try:
            await handler(message, data)
        finally:
            await super().close_session(data)


class OnPrivateCbqDBInit(DatabaseInitMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       cbq: CallbackQuery,
                       data: Dict[str, Any]):
        session: AsyncSession = self.session_pool()
        data["session"] = session
        data["bot_pickle"] = self.bot_pickle
        data["scheduler"] = self.scheduler

        super().create_contexts(data, session)

        await super().set_user_to_contexts(data, cbq.from_user)

        try:
            await handler(cbq, data)
        finally:
            await super().close_session(data)

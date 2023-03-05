from typing import Dict, Any, Callable, Awaitable

from aiogram.types import CallbackQuery, ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares.database_init.base import DatabaseInitMiddleware


class OnChannelMyChatMemberDBInit(DatabaseInitMiddleware):
    async def __call__(self, handler: Callable[[ChatMemberUpdated, Dict[str, Any]], Awaitable[Any]],
                       my_chat_member: ChatMemberUpdated,
                       data: Dict[str, Any]):
        session: AsyncSession = self.session_pool()
        data["session"] = session
        data["bot_pickle"] = self.bot_pickle
        data["scheduler"] = self.scheduler

        super().create_contexts(data, session)

        try:
            print(f'{self.__class__} ok')
            await handler(my_chat_member, data)
        finally:
            await super().close_session(data)


class OnChannelCbqDBInit(DatabaseInitMiddleware):
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

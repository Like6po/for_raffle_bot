from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.contexts.user import UserContext
from database.models.user import User
from database.contexts.channel import ChannelContext
from database.models.channel import Channel
from database.contexts.user_channel import UserChannelContext
from database.models.user_channel import UserChannel
from database.contexts.member import MemberContext
from database.models.member import Member


class InitMiddleware(BaseMiddleware):
    def __init__(self, session_pool, bot: Bot):
        self.session_pool = session_pool
        self.bot = bot
        super().__init__()

    @classmethod
    async def close_session(cls, data: Dict[str, Any]):
        if session := data.get("session", None):
            session: AsyncSession
            await session.close()

    def create_contexts(self, data: Dict[str, Any], session: AsyncSession):
        data["bot"] = self.bot
        data["user_db"] = UserContext(session, query_model=User)
        data["channel_db"] = ChannelContext(session, query_model=Channel)
        data["member_db"] = MemberContext(session, query_model=Member)
        data["user_channels_db"] = UserChannelContext(session, query_model=UserChannel)

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       obj: TelegramObject,
                       data: Dict[str, Any]):
        session: AsyncSession = self.session_pool()

        data["session"] = session

        self.create_contexts(data, session)
        await handler(obj, data)

        await self.close_session(data)

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types.user import User as AiogramUser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from database.contexts import ContestContext, ContestMemberContext, MemberContext, UserChannelContext, \
    ChannelContext, UserContext
from database.models import ContestMember, Contest, Member, UserChannel, Channel, User


class DatabaseInitMiddleware(BaseMiddleware):
    def __init__(self, session_pool, bot_pickle, scheduler: AsyncIOScheduler):
        self.session_pool = session_pool
        self.bot_pickle = bot_pickle
        self.scheduler = scheduler
        super().__init__()

    @classmethod
    def create_contexts(cls, data: Dict[str, Any], session: AsyncSession):
        data["user_db"] = UserContext(session, query_model=User)
        data["channel_db"] = ChannelContext(session, query_model=Channel)
        data["member_db"] = MemberContext(session, query_model=Member)
        data["user_channels_db"] = UserChannelContext(session, query_model=UserChannel)
        data["contest_db"] = ContestContext(session, query_model=Contest)
        data["contest_members_db"] = ContestMemberContext(session, query_model=ContestMember)

    @classmethod
    async def close_session(cls, data: Dict[str, Any]):
        await data["user_db"]._session.close()
        await data["channel_db"]._session.close()
        await data["member_db"]._session.close()
        await data["user_channels_db"]._session.close()
        await data["contest_db"]._session.close()
        await data["contest_members_db"]._session.close()

        if session := data.get("session", None):
            session: AsyncSession
            await session.close()

    @classmethod
    async def set_user_to_contexts(cls, data: Dict[str, Any], user: AiogramUser):
        if user.is_bot:
            data["user_data"] = None
            return
        data["user_db"].user = user
        data["user_data"] = await data["user_db"].get_or_create_and_get()

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       obj: TelegramObject,
                       data: Dict[str, Any]):
        session: AsyncSession = self.session_pool()
        data["session"] = session
        data["bot_pickle"] = self.bot_pickle
        data["scheduler"] = self.scheduler
        await handler(obj, data)

        await self.close_session(data)

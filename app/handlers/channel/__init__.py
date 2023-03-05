from aiogram import Router
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from filters.chat_type import ChannelChatFilter
from handlers.channel.chat_member.base import new_channel
from handlers.channel.contest.callbacks.base import contest_join
from keyboards.contest import JoinButtonCallback
from middlewares.database_init.channel import OnChannelCbqDBInit, OnChannelMyChatMemberDBInit
from middlewares.database_upd.channel import OnChannelCbqDBUpd


def create_channel_router(session_pool, bot_pickle, scheduler: AsyncIOScheduler) -> Router:
    r: Router = Router(name="channel_router")

    r.my_chat_member.bind_filter(bound_filter=ChannelChatFilter)
    r.callback_query.bind_filter(bound_filter=ChannelChatFilter)

    r.my_chat_member.middleware(OnChannelMyChatMemberDBInit(session_pool, bot_pickle, scheduler))
    r.callback_query.middleware(OnChannelCbqDBInit(session_pool, bot_pickle, scheduler))
    r.callback_query.middleware(OnChannelCbqDBUpd())

    r.my_chat_member.register(new_channel)
    r.callback_query.register(contest_join, JoinButtonCallback.filter())

    return r

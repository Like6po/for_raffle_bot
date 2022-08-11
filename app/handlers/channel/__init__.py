from aiogram import Router, Bot

from filters.chat_type import ChannelChatFilter
from handlers.channel.chat_member.base import new_channel
from handlers.channel.contest.callbacks.base import contest_join
from keyboards.contest import JoinButtonCallback
from middlewares.init_contexts import InitMiddleware


def create_channel_router(session_pool, bot: Bot) -> Router:
    r: Router = Router(name="channel_router")

    r.my_chat_member.bind_filter(bound_filter=ChannelChatFilter)
    r.callback_query.bind_filter(bound_filter=ChannelChatFilter)

    r.my_chat_member.middleware(InitMiddleware(session_pool, bot))
    r.callback_query.middleware(InitMiddleware(session_pool, bot))

    r.my_chat_member.register(new_channel)
    r.callback_query.register(contest_join, JoinButtonCallback.filter())

    return r

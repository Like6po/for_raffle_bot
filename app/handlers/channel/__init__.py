from aiogram import Router, Bot

from filters.chat_type import ChannelChatFilter
from middlewares.init_contexts import InitMiddleware
from handlers.channel.chat_member.base import new_channel


def create_channel_router(session_pool, bot: Bot) -> Router:
    r: Router = Router(name="channel_router")

    r.my_chat_member.bind_filter(bound_filter=ChannelChatFilter)
    r.my_chat_member.middleware(InitMiddleware(session_pool, bot))
    r.my_chat_member.register(new_channel)

    return r

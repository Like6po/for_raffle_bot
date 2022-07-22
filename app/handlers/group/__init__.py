from aiogram import Router, Bot

from filters.chat_type import ChannelChatFilter
from middlewares.init_contexts import InitMiddleware
from .new_group.base import new_group


def create_group_router(session_pool, bot: Bot) -> Router:
    group_router: Router = Router(name="group_router")

    group_router.my_chat_member.bind_filter(bound_filter=ChannelChatFilter)
    group_router.my_chat_member.middleware(InitMiddleware(session_pool, bot))
    group_router.my_chat_member.register(new_group)

    return group_router

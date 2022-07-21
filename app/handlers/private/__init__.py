from aiogram import Router, Bot

from filters.chat_type import PrivateChatFilter
from middlewares.init_contexts import InitMiddleware
from .start.base import command_start


def create_private_router(session_pool, bot: Bot) -> Router:
    private_router: Router = Router(name="private_router")

    # Сообщения

    private_router.message.bind_filter(bound_filter=PrivateChatFilter)
    private_router.message.middleware(InitMiddleware(session_pool, bot))
    private_router.message.register(command_start,
                                    commands=["start"])
    return private_router

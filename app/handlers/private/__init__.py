from aiogram import Router

from filters.chat_type import PrivateChatFilter
from .start.base import command_start


def create_private_router(sqlalchemy_session_pool) -> Router:
    private_router: Router = Router(name="private_router")

    # Сообщения

    private_router.message.bind_filter(bound_filter=PrivateChatFilter)

    private_router.message.register(command_start,
                                    commands=["start"])
    return private_router

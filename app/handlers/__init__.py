from aiogram import Dispatcher, Bot

from handlers.channel import create_channel_router
from handlers.group import create_group_router
from handlers.private import create_private_router


def register_routers(dp: Dispatcher, session_pool, bot: Bot):
    dp.include_router(create_private_router(session_pool, bot))
    dp.include_router(create_group_router(session_pool, bot))
    dp.include_router(create_channel_router(session_pool, bot))

from aiogram import Dispatcher

from .group import create_group_router
from .private import create_private_router


def register_routers(dp: Dispatcher, sqlalchemy_session_pool):
    dp.include_router(create_private_router(sqlalchemy_session_pool))

    dp.include_router(create_group_router())

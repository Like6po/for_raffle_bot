from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.channel import create_channel_router
from handlers.private import create_private_router


def register_routers(dp: Dispatcher, session_pool, bot_pickle, scheduler: AsyncIOScheduler):
    dp.include_router(create_private_router(session_pool, bot_pickle, scheduler))
    dp.include_router(create_channel_router(session_pool, bot_pickle, scheduler))

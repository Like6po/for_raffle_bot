from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.channel import create_channel_router
from handlers.private import create_private_router
from misc.config import config
from .errors import errors


def register_routers(dp: Dispatcher, session_pool, bot_pickle, scheduler: AsyncIOScheduler):
    dp.include_router(create_private_router(session_pool, bot_pickle, scheduler))
    dp.include_router(create_channel_router(session_pool, bot_pickle, scheduler))

    if config.tg_bot.report_chat_id and config.tg_bot.is_report_handler_error:
        dp.errors.register(errors)

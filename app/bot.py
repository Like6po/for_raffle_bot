import asyncio
import logging
import pickle

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aioredis import Redis
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.models import DatabaseModel
from handlers import register_routers
from misc.config import config
from misc.set_bot_commands import set_bot_commands

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-5s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting app")

    # tg stuff
    storage = RedisStorage(redis=Redis(host=config.redis.host,
                                       port=config.redis.port,
                                       db=1))
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    bot_pickle = pickle.dumps(bot)
    dp = Dispatcher(storage=storage)

    # scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_jobstore(RedisJobStore(host=config.redis.host,
                                         port=config.redis.port,
                                         db=2,
                                         pickle_protocol=pickle.DEFAULT_PROTOCOL))
    scheduler.start()

    engine = create_async_engine(
        config.db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=100,
        max_overflow=200,
        future=True,
        echo=False
    )
    async with engine.begin() as conn:
        # await conn.run_sync(DatabaseModel.metadata.drop_all)
        await conn.run_sync(DatabaseModel.metadata.create_all)

    await set_bot_commands(bot)
    sqlalchemy_session_pool = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    register_routers(dp, sqlalchemy_session_pool, bot_pickle, scheduler)

    # start
    try:
        await bot.get_updates(-1)
        await dp.start_polling(bot,
                               allowed_updates=["message",
                                                "edited_message",
                                                "callback_query",
                                                "my_chat_member",
                                                "chat_member"])
    finally:
        await storage.close()

        await bot.session.close()
        await engine.dispose()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

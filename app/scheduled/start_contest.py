import pickle

from aiogram import Bot
from apscheduler.jobstores.redis import RedisJobStore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts import ContestContext
from database.models import Contest
from keyboards.contest import post_button_kb
from misc.config import config
from misc.utils.contest import send_post


async def start_contest(bot, channel_data, contest_data: Contest, state_data: dict):
    engine = create_async_engine(
        config.db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=3,
        max_overflow=2,
        future=True,
        echo=False,
        connect_args={"server_settings": {"application_name": "bot_settings_updater"}}
    )
    try:
        storage = RedisJobStore(host=config.redis.host,
                                port=config.redis.port,
                                db=2,
                                pickle_protocol=pickle.DEFAULT_PROTOCOL)
        bot: Bot = pickle.loads(bot)
        session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
        try:
            contest_db = ContestContext(session_or_pool=session, query_model=Contest)
            if not await contest_db.get_by_db_id(contest_data.id):
                print('конкурс был удален')
            else:
                await send_post(bot, channel_data.tg_id, state_data,
                                post_button_kb(state_data['btn_title'], contest_data.id), True, contest_db, contest_data)
            storage.remove_job(f'start_contest_{contest_data.id}')
        finally:
            storage.shutdown()
            await bot.session.close()
            session.close_all()
    finally:
        await engine.dispose()

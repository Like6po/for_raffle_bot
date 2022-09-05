import pickle

from aiogram import Bot
from apscheduler.jobstores.redis import RedisJobStore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts import ContestContext, ContestMemberContext, MemberContext
from database.models import Contest, ContestMember, Member
from misc.config import config
from misc.utils.contest import choose_the_winners


async def close_contest(bot, contest_data: Contest):
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
            contest_members_db = ContestMemberContext(session_or_pool=session, query_model=ContestMember)
            member_db = MemberContext(session_or_pool=session, query_model=Member)
            if not await contest_db.get_by_db_id(contest_data.id):
                return print('конкурс был удален')
            else:
                await choose_the_winners(bot, contest_db, contest_members_db, member_db, contest_data.id)
            storage.remove_job(f'close_contest_{contest_data.id}')
        finally:
            storage.shutdown()
            await bot.session.close()
            session.close_all()
    finally:
        await engine.dispose()

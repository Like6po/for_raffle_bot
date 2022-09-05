from datetime import datetime

from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.contexts import ContestContext, ChannelContext, ContestMemberContext
from keyboards.results import results_kb, ResultsDeleteContestCallback
from misc.utils.texts import make_text_of_created_contests_with_pagination


async def contest_results_delete_contest_cbq(cbq: CallbackQuery,
                                             callback_data: ResultsDeleteContestCallback,
                                             channel_db: ChannelContext,
                                             contest_db: ContestContext,
                                             contest_members_db: ContestMemberContext,
                                             scheduler: AsyncIOScheduler):
    if contest_data := await contest_db.get_by_db_id(callback_data.contest_db_id):
        await contest_db.finish(callback_data.contest_db_id)
        await contest_members_db.finish_contest(callback_data.contest_db_id)

        if contest_data.start_at and contest_data.start_at > datetime.now():
            scheduler.remove_job(f'start_contest_{contest_data.id}')

        if contest_data.end_at and contest_data.end_at > datetime.now():
            scheduler.remove_job(f'close_contest_{contest_data.id}')

        await cbq.answer('Конкурс успешно удален.\nПримечание: пост с конкурсом не был удален.', show_alert=True)
    else:
        await cbq.answer('Конкурс не найден.', show_alert=True)

    await cbq.message.edit_text(make_text_of_created_contests_with_pagination(
        await channel_db.get(channel_id=callback_data.channel_db_id),
        contest_list := await contest_db.get(callback_data.channel_db_id, offset=callback_data.page * 10),
        count := await contest_db.count(callback_data.channel_db_id),
        page=callback_data.page + 1),
        reply_markup=results_kb(contest_list, count, callback_data.channel_db_id, callback_data.page)
    )

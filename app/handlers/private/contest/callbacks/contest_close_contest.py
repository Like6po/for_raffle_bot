from aiogram import Bot
from aiogram.types import CallbackQuery

from database.contexts import ContestMemberContext, MemberContext
from database.contexts.channel import ChannelContext
from database.contexts.contest import ContestContext
from keyboards.results import ResultsCallback
from keyboards.results import results_kb
from misc.contest import choose_the_winners
from misc.texts import make_text_of_created_contests_with_pagination


async def contest_close_cbq(cbq: CallbackQuery,
                            bot: Bot,
                            callback_data: ResultsCallback,
                            contest_db: ContestContext,
                            channel_db: ChannelContext,
                            contest_members_db: ContestMemberContext,
                            member_db: MemberContext):
    await choose_the_winners(bot, contest_db, contest_members_db, member_db, callback_data.contest_db_id)

    await cbq.message.edit_text(make_text_of_created_contests_with_pagination(
            await channel_db.get(channel_id=callback_data.channel_db_id),
            contest_list := await contest_db.get(callback_data.channel_db_id, offset=callback_data.page * 10),
            count := await contest_db.count(callback_data.channel_db_id),
            page=callback_data.page + 1),
        reply_markup=results_kb(contest_list, count, callback_data.channel_db_id, callback_data.page + 1)
    )
    await cbq.answer(f'Успешно закончил конкурс #{callback_data.contest_db_id}.', show_alert=True)

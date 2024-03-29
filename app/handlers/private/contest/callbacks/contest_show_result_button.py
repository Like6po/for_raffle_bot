from aiogram.types import CallbackQuery

from database.contexts import ContestContext, ChannelContext, ContestMemberContext
from keyboards.contest import ContestCallback
from keyboards.results import results_kb
from misc.utils.texts import make_text_of_created_contests_with_pagination


async def choose_contest_to_finish_cbq(cbq: CallbackQuery,
                                       callback_data: ContestCallback,
                                       channel_db: ChannelContext,
                                       contest_db: ContestContext,
                                       contest_members_db: ContestMemberContext):
    if (count := await contest_db.count(callback_data.channel_id)) <= 0:
        return await cbq.answer('У вас отсутствуют активные конкурсы.', show_alert=True)

    await cbq.message.edit_text(await make_text_of_created_contests_with_pagination(
            await channel_db.get(channel_id=callback_data.channel_id),
            contest_list := await contest_db.get(callback_data.channel_id),
            contest_members_db,
            count),
        reply_markup=results_kb(contest_list, count, callback_data.channel_id)
    )
    await cbq.answer()

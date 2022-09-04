from aiogram.types import CallbackQuery

from database.contexts import ContestContext, ChannelContext
from keyboards.results import results_kb, ResultsChangePageCallback
from misc.texts import make_text_of_created_contests_with_pagination


async def contest_results_change_page_cbq(cbq: CallbackQuery,
                                          callback_data: ResultsChangePageCallback,
                                          channel_db: ChannelContext,
                                          contest_db: ContestContext):
    if (count := await contest_db.count(callback_data.channel_db_id)) <= 0:
        return await cbq.answer('У вас отсутствуют активные конкурсы.', show_alert=True)

    await cbq.message.edit_text(make_text_of_created_contests_with_pagination(
            await channel_db.get(channel_id=callback_data.channel_db_id),
            contest_list := await contest_db.get(callback_data.channel_db_id, offset=callback_data.page * 10),
            count,
            page=callback_data.page + 1),
        reply_markup=results_kb(contest_list, count, callback_data.channel_db_id, callback_data.page)
    )
    await cbq.answer()

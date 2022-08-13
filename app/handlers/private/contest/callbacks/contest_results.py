from aiogram.types import CallbackQuery

from database.contexts import ContestContext
from keyboards.contest import ContestCallback
from keyboards.results import results_kb


async def choose_contest_to_finish(cbq: CallbackQuery,
                                   callback_data: ContestCallback,
                                   contest_db: ContestContext):
    if len(contest_list := await contest_db.get_all(callback_data.channel_id)) <= 0:
        return await cbq.answer('У вас отсутствуют активные конкурсы.')

    await cbq.message.edit_reply_markup(
        results_kb(contest_list, callback_data.channel_id)
    )
    await cbq.answer()

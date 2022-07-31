from aiogram.types import CallbackQuery

from misc.pages import array_to_pages
from database.contexts.user_channel import UserChannelContext
from keyboards.contest import channels_choice_kb
from keyboards.base import back_kb


async def start_contest(cbq: CallbackQuery,
                        user_channels_db: UserChannelContext):
    user_channels_list = await user_channels_db.get_all_user_channels(cbq.from_user)

    if not user_channels_list:
        return await cbq.message.edit_text("Вы ещё не привязали ни одного канала!",
                                           reply_markup=back_kb())

    await cbq.message.edit_text("Выберите канал:",
                                reply_markup=channels_choice_kb(
                                    channels_page=array_to_pages(user_channels_list)))

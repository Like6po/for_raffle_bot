from aiogram.types import CallbackQuery

from database.contexts.user_channel import UserChannelContext
from keyboards.contest import channels_choice_kb, ContestCallback
from misc.utils.pages import array_to_pages


async def contest_channel_switch(cbq: CallbackQuery,
                                 callback_data: ContestCallback,
                                 user_channels_db: UserChannelContext):
    user_channels_list = await user_channels_db.get_all_user_channels(cbq.from_user)
    await cbq.message.edit_text("Выберите канал:",
                                reply_markup=channels_choice_kb(
                                    channels_page=array_to_pages(user_channels_list),
                                    page_index=callback_data.page_index))

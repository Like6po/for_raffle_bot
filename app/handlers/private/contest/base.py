from aiogram.types import Message

from misc.pages import array_to_pages
from database.contexts.user_channel import UserChannelContext
from keyboards.contest import channels_choice_kb
from keyboards.channels import channels_cancel_kb


async def command_contest(message: Message,
                          user_channels_db: UserChannelContext):
    user_channels_list = await user_channels_db.get_all_user_channels(message.from_user)

    if not user_channels_list:
        return await message.answer("Вы ещё не привязали ни одного канала!",
                                           reply_markup=channels_cancel_kb())

    await message.answer("Выберите канал:",
                                reply_markup=channels_choice_kb(
                                    channels_page=array_to_pages(user_channels_list)))

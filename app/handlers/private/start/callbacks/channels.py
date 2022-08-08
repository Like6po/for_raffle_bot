from aiogram.types import CallbackQuery

from database.contexts.user_channel import UserChannelContext
from keyboards.channels import channels_kb
from misc.links import chat_link


async def start_channels(cbq: CallbackQuery,
                         user_channels_db: UserChannelContext):
    user_channels_list = await user_channels_db.get_all_user_channels(cbq.from_user)
    if not user_channels_list:
        return await cbq.message.edit_text("Вы ещё не привязали ни одного канала!",
                                           reply_markup=channels_kb())

    user_channels = [f"{index + 1}. {chat_link(username=channel.username, tg_id=channel.tg_id, title=channel.title)}"
                     for index, channel in enumerate(user_channels_list)]

    await cbq.message.edit_text("Привязанные каналы:\n\n" + "\n".join(user_channels),
                                disable_web_page_preview=True,
                                reply_markup=channels_kb())

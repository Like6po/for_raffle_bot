from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, Chat
from aiogram.utils.markdown import hbold

from database.contexts.channel import ChannelContext
from database.contexts.user_channel import UserChannelContext
from keyboards.channels import channels_kb
from misc.utils.links import chat_link


async def wait_channel_to_update(message: Message,
                                 state: FSMContext,
                                 bot: Bot,
                                 channel_db: ChannelContext,
                                 user_channels_db: UserChannelContext):
    channel: Chat | None = None

    if message.forward_from_chat:
        channel = message.forward_from_chat
    elif message.text.startswith('@'):
        try:
            channel = await bot.get_chat(message.text)
        except TelegramBadRequest as e:
            if e.message.startswith('Bad Request: chat not found'):
                return await message.reply('Такого канала не существует, либо он не зарегистрирован!')
    else:
        await message.answer("Ожидаю либо юзернейм канала, либо пересланное с канала сообщение! Попробуйте снова!")
        return

    if not await channel_db.get(tg_id=channel.id):
        return await message.reply('Этот канал не зарегистрирован.')

    await channel_db.update(tg_id=channel.id, username=channel.username, title=channel.title)

    await state.clear()

    user_channels_list = await user_channels_db.get_all_user_channels(message.from_user)

    user_channels = [f"{index + 1}. {chat_link(username=channel.username, tg_id=channel.id, title=channel.title)}"
                     for index, channel in enumerate(user_channels_list)]

    await message.answer(f"Отлично! Канал {hbold(channel.title)} успешно обновлен!\n\n"
                         f"Привязанные каналы:\n\n" + "\n".join(user_channels),
                         disable_web_page_preview=True,
                         reply_markup=channels_kb())

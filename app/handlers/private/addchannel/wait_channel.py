from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from database.contexts.channel import ChannelContext
from database.contexts.user import UserContext
from database.contexts.user_channel import UserChannelContext
from database.models.channel import Channel
from database.models.user import User
from keyboards.channels import channels_kb
from misc.links import chat_link


async def wait_channel(message: Message,
                       state: FSMContext,
                       bot: Bot,
                       user_db: UserContext,
                       channel_db: ChannelContext,
                       user_channels_db: UserChannelContext):
    channel: Channel | None = None

    if message.forward_from_chat:
        channel = await channel_db.get(message.forward_from_chat)
    elif message.text.startswith('@'):
        try:
            channel = await channel_db.get(await bot.get_chat(message.text))
        except TelegramBadRequest as e:
            if e.message.startswith('Bad Request: chat not found'):
                return await message.reply('Такого канала не существует.')
    else:
        await message.answer("Ожидаю либо юзернейм канала, либо пересланное с канала сообщение! Попробуйте снова!")
        return

    if not channel:
        await message.answer("Пригласите меня в канал и выдайте мне права на публикацию сообщений! "
                             "Попробуйте снова!")
        return

    try:
        if (await bot.get_chat_member(channel.tg_id, message.from_user.id)).status not in ['creator', 'administrator']:
            await message.answer(f"Вы не являетесь администратором канала! Попробуйте снова!")
            return

        if not (await bot.get_chat_member(channel.tg_id, bot.id)).can_post_messages:
            await message.answer("Выдайте мне права на публикацию сообщений в канале! Попробуйте снова!")
            return

    except TelegramForbiddenError:
        await message.answer("Пригласите бота в канал и выдайте ему права администратора! Попробуйте снова!")

    user: User = await user_db.get_or_create_and_get(message.from_user)
    if not await user_channels_db.check_exists(user.id, channel.id):
        await user_channels_db.new(user.id, channel.id)

    await state.clear()

    user_channels_list = await user_channels_db.get_all_user_channels(message.from_user)

    user_channels = [f"{index + 1}. {chat_link(username=channel.username, tg_id=channel.tg_id, title=channel.title)}"
                     for index, channel in enumerate(user_channels_list)]

    await message.answer(f"Отлично! Канал {hbold(channel.title)} успешно привязан!\n\n"
                         f"Привязанные каналы:\n\n" + "\n".join(user_channels),
                         disable_web_page_preview=True,
                         reply_markup=channels_kb())

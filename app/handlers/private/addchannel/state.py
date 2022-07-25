from aiogram.types import Message
from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError

from database.contexts.user import UserContext
from database.contexts.channel import ChannelContext
from database.contexts.user_channel import UserChannelContext


async def state_addchannel(message: Message, state: FSMContext,
                           bot: Bot, user_db: UserContext,
                           channel_db: ChannelContext, user_channels_db: UserChannelContext):
    await state.clear()

    if message.text.startswith('@'):
        channel = await channel_db.get(await bot.get_chat(message.text))
    elif message.forward_from_chat:
        channel = await channel_db.get(message.forward_from_chat)
    else:
        return

    try:
        if channel:
            user = await user_db.get(message.from_user)
            is_user_admin = (await bot.get_chat_member(channel.tg_id, message.from_user.id)).status in ['creator', 'administrator']
            if is_user_admin:
                await user_channels_db.check_and_create(user, channel)
                await message.answer(f"Отлично! Вы привязаны к каналу: {channel.title}")
            else:
                await message.answer(f"Вы не являетесь администратором канала!")
        else:
            await message.answer("Пригласите бота в канал и выдайте ему права администратора!")
    except TelegramForbiddenError:
        await message.answer("Пригласите бота в канал и выдайте ему права администратора!")

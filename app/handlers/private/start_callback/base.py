from aiogram import Bot
from aiogram.types import CallbackQuery
from keyboards.start import channels_kb

from database.contexts.user_channel import UserChannelContext
from database.contexts.channel import ChannelContext
from database.contexts.user import UserContext


async def start_channels(cbq: CallbackQuery, bot: Bot,
                         user_channels_db: UserChannelContext,
                         user_db: UserContext, channel_db: ChannelContext):
    user = await user_db.get(cbq.from_user)

    channel_contexts = [await channel_db.get(channel_id=channel_context.channel_id) for channel_context in await user_channels_db.get(user)]
    user_channels = [f"{index+1}. <a href='t.me/{channel.username}'>{channel.title}</a>" for index, channel in enumerate(channel_contexts)]

    if user_channels:
        await cbq.message.edit_text("Привязанные каналы:\n\n" + "\n".join(user_channels),
                                    disable_web_page_preview=True)
    else:
        await cbq.message.edit_text("Вы ещё не привязали ни одного канала!")

    await cbq.message.edit_reply_markup(reply_markup=channels_kb())
    await bot.answer_callback_query(cbq.id)

from aiogram.types.chat_member_updated import ChatMemberUpdated

from database.contexts.channel import ChannelContext


async def new_channel(chat: ChatMemberUpdated, channel_db: ChannelContext):
    await channel_db.get_or_create_and_get(chat.chat)
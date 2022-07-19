from dataclasses import dataclass

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import TelegramObject, Message, CallbackQuery


@dataclass
class ChatType:
    PRIVATE = 'private'
    GROUP = 'group'
    SUPERGROUP = 'supergroup'
    CHANNEL = 'channel'


class ChatFilter(BaseFilter):
    chat_type: str

    async def __call__(self, obj: TelegramObject):
        if isinstance(obj, Message):
            return obj.chat.type == self.chat_type
        if isinstance(obj, CallbackQuery):
            return obj.message.chat.type == self.chat_type
        return False


class PrivateChatFilter(ChatFilter):
    def __init__(self, **kwargs):
        super().__init__(chat_type=ChatType.PRIVATE, **kwargs)


class SuperGroupChatFilter(ChatFilter):
    def __init__(self, **kwargs):
        super().__init__(chat_type=ChatType.SUPERGROUP, **kwargs)


class GroupChatFilter(ChatFilter):
    def __init__(self, **kwargs):
        super().__init__(chat_type=ChatType.GROUP, **kwargs)


class ChannelChatFilter(ChatFilter):
    def __init__(self, **kwargs):
        super().__init__(chat_type=ChatType.CHANNEL, **kwargs)

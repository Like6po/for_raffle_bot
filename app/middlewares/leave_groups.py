from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import TelegramObject, Message, CallbackQuery, ChatMemberUpdated


class LeaveGroupsMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       obj: TelegramObject,
                       data: Dict[str, Any]):
        bot: Bot = data['bot']

        if isinstance(obj, Message):
            chat_id = obj.chat.id
        elif isinstance(obj, CallbackQuery):
            chat_id = obj.message.chat.id
        elif isinstance(obj, ChatMemberUpdated):
            chat_id = obj.chat.id
        else:
            return

        try:
            await bot.send_message(chat_id, 'Я не предназначен для групп! '
                                            'Пожалуйста, прочтите инструкцию в канале автора: https://t.me/bots_tikey',
                                   disable_web_page_preview=True)
            return await bot.leave_chat(chat_id=chat_id)
        except TelegramAPIError:
            return

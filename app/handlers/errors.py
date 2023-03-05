import asyncio
import logging
from traceback import format_exc

from aiogram import Bot
from aiogram import html
from aiogram.exceptions import DetailedAiogramError, TelegramBadRequest, TelegramRetryAfter
from aiogram.types import Update

from misc.config import config


async def errors(update: Update,
                 bot: Bot,
                 exception: DetailedAiogramError):
    if isinstance(exception, TelegramRetryAfter):
        if exception.message.startswith("Flood control exceeded"):
            seconds = exception.retry_after
            return await update.callback_query.answer(
                    f'⚠ Ошибка редактирования сообщения. Попробуйте снова через {seconds}с',
                    show_alert=True,
                    cache_time=seconds + 2)

    elif isinstance(exception, TelegramBadRequest):
        if exception.message.startswith('Bad Request: message is not modified'):
            if update.callback_query:
                return await update.callback_query.answer(
                    '⚠ Произошла непредвиденная ошибка. Подождите пару секунд.',
                    show_alert=True,
                    cache_time=2
                )

    if update.callback_query:
        title = update.callback_query.message.chat.title or update.callback_query.from_user.full_name
        chat_id = update.callback_query.message.chat.id
        username = update.callback_query.message.chat.username
        link = update.callback_query.message.chat.invite_link
        msg = update.callback_query.message
    else:
        title = update.message.chat.title or update.message.from_user.full_name
        chat_id = update.message.chat.id
        username = update.message.chat.username
        link = update.message.chat.invite_link
        msg = update.message

    text = f'{title} ({chat_id}, @{username}, {link}) '\
           f'ошибка: {exception.__class__}\n\n' \
           f'{format_exc()}\n' \
           f'{msg.chat}\n\n' \
           f'{msg.from_user}\n\n' \
           f'{msg.text=}'

    text = html.quote(text)

    for i in range(0, len(text), 4095):
        await bot.send_message(config.tg_bot.report_chat_id,
                               text[i:i+4095],
                               disable_notification=True)
        await asyncio.sleep(0.5)

    logging.error(msg=f"Ошибка {type(exception)}", exc_info=exception)

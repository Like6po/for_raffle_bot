from aiogram import Bot
from aiogram.types import Message

from datetime import datetime


def get_content(message: Message, last_state: str):
    if last_state == 'text':
        return message.html_text

    elif last_state == 'btn_title':
        return message.text

    elif last_state == 'attachment_hash':
        if message.photo:
            return f"{message.photo[-1].file_id}:photo"
        if message.document:
            return f"{message.document.file_id}:document"
        return None

    elif last_state in ['winner_count', 'end_count']:
        try:
            return int(message.text)
        except:
            return None

    elif last_state in ['start_at', 'end_at']:
        try:
            return datetime.strptime(message.text, '%H:%M %d.%m.%Y')
        except:
            return None


async def send_post(bot: Bot, chat_id: int, state_data: dict, reply_markup=None):
    if not state_data['attachment_hash']:
        await bot.send_message(chat_id=chat_id, text=state_data['text'], parse_mode='HTML',
                               reply_markup=reply_markup,
                               disable_web_page_preview=state_data['is_attachment_preview'])
        return

    file_type = state_data['attachment_hash'].split(':')[-1]
    if file_type == 'photo':
        await bot.send_photo(chat_id=chat_id, photo=state_data['attachment_hash'].split(':')[0],
                             caption=state_data['text'],
                             parse_mode='HTML', reply_markup=reply_markup)
    elif file_type == 'document':
        await bot.send_document(chat_id=chat_id, document=state_data['attachment_hash'].split(':')[0],
                                caption=state_data['text'],
                                parse_mode='HTML', reply_markup=reply_markup)

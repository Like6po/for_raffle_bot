from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class StartCallback(CallbackData, prefix="start"):
    action: str


def start_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='📝 Новости бота',
                                    url='http://t.me/bots_TiKey'))

    return kb_obj.as_markup()

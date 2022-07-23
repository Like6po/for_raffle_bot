from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ContestCallback(CallbackData, prefix="contest"):
    action: str


def contest_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='Участвовать',
                                    callback_data=ContestCallback(action="join").pack()))

    return kb_obj.as_markup()

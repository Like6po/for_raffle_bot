from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.channels import ChannelsCallback


def back_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='⏪ Назад',
                                    callback_data=ChannelsCallback(action="back").pack()))
    return kb_obj.as_markup()

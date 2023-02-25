from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ChannelsCallback(CallbackData, prefix="channels"):
    action: str


def channels_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='🔗 Привязать',
                                    callback_data=ChannelsCallback(action="add").pack()))
    kb_obj.row(InlineKeyboardButton(text='🆙 Обновить данные',
                                    callback_data=ChannelsCallback(action="update").pack()))
    kb_obj.row(InlineKeyboardButton(text='⏪ Назад',
                                    callback_data=ChannelsCallback(action="back").pack()))
    return kb_obj.as_markup()


def channels_cancel_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='⏪ Отмена',
                                    callback_data=ChannelsCallback(action="cancel").pack()))
    return kb_obj.as_markup()

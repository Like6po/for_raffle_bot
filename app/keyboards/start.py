from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ChannelsCallback(CallbackData, prefix="channels"):
    action: str


class StartCallback(CallbackData, prefix="start"):
    action: str


def start_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='💬 Каналы',
                                    callback_data=StartCallback(action="channels").pack()),
               InlineKeyboardButton(text='🎁 Создать Конкурс',
                                    callback_data=StartCallback(action="contest").pack()))
    kb_obj.row(InlineKeyboardButton(text='📋 Инструкция',
                                    url='https://t.me/bots_TiKey'),
               InlineKeyboardButton(text='📝 Новости бота',
                                    url='https://t.me/bots_TiKey'))
    kb_obj.row(InlineKeyboardButton(text='🖥 Исходный код',
                                    url='https://github.com/Like6po/for_raffle_bot'))


def channels_kb():
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='🔗 Привязать',
                                    callback_data=ChannelsCallback(action="add").pack()))
    kb_obj.row(InlineKeyboardButton(text='⏪ Назад',
                                    callback_data=ChannelsCallback(action="back").pack()))
    return kb_obj.as_markup()
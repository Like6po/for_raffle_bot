from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.channels import ChannelsCallback
from keyboards.start import StartCallback


class ContestCallback(CallbackData, prefix="contest"):
    action: str
    page_index: int = 0
    channel_id: int = None
    last_state: str = None
    condition: bool = None


def channels_choice_kb(channels_page: list, page_index: int = 0):
    kb_obj = InlineKeyboardBuilder()
    for channel in channels_page[page_index]:
        kb_obj.row(InlineKeyboardButton(text=channel.title,
                                        callback_data=ContestCallback(action="channel_choice",
                                                                      channel_id=channel.id).pack()))

    keyb_btns = []
    if (index := page_index - 1) >= 0:
        keyb_btns.append(
            InlineKeyboardButton(text=f'⏪\n{index + 1} стр.', callback_data=ContestCallback(action="channel_switch",
                                                                                            page_index=index).pack()))
    if len(channels_page) > (index := page_index + 1):
        keyb_btns.append(
            InlineKeyboardButton(text=f'⏩\n{index + 1} стр.', callback_data=ContestCallback(action="channel_switch",
                                                                                            page_index=index).pack()))
    kb_obj.row(*keyb_btns)

    kb_obj.row(InlineKeyboardButton(text='❌ Назад', callback_data=ChannelsCallback(action="back").pack()))

    return kb_obj.as_markup()


def post_button_kb(button_title: str):
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text=button_title or 'Учавствовать',
                                    callback_data=ContestCallback(action="join").pack()))

    return kb_obj.as_markup()


def contest_action_kb(channel_id: int, contest_results_btn: bool = True):
    kb_obj = InlineKeyboardBuilder()
    kb_obj.row(InlineKeyboardButton(text='➕ Создать Конкурс',
                                    callback_data=ContestCallback(action="create", channel_id=channel_id).pack()))
    if contest_results_btn:
        kb_obj.row(InlineKeyboardButton(text='📝 Подвести Итоги',
                                        callback_data=ContestCallback(action="results").pack()))
    kb_obj.row(InlineKeyboardButton(text='🗄 Выбор Каналов',
                                    callback_data=StartCallback(action="contest").pack()))

    return kb_obj.as_markup()


def contest_kb(channel_id: int, last_state: str = None, condition_buttons_title: tuple | list = None):
    kb_obj = InlineKeyboardBuilder()
    if condition_buttons_title:
        keyb_btns = [InlineKeyboardButton(text=condition_buttons_title[0],
                                          callback_data=ContestCallback(action="condition", condition=True,
                                                                        last_state=last_state,
                                                                        channel_id=channel_id).pack())]
        if len(condition_buttons_title) == 2:
            keyb_btns.append(InlineKeyboardButton(text=condition_buttons_title[1],
                                                  callback_data=ContestCallback(action="condition", condition=False,
                                                                                last_state=last_state,
                                                                                channel_id=channel_id).pack()))
        kb_obj.row(*keyb_btns)

    kb_obj.row(InlineKeyboardButton(text='⏪ Назад',
                                    callback_data=ContestCallback(action="return" if last_state else "channel_choice",
                                                                  last_state=last_state, channel_id=channel_id).pack()))
    return kb_obj.as_markup()

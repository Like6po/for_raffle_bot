from html import unescape
from typing import List

from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Contest
from keyboards.contest import ContestCallback


class ResultsCallback(CallbackData, prefix="results"):
    contest_db_id: int
    channel_db_id: int
    page: int


class ResultsChangePageCallback(CallbackData, prefix="results"):
    channel_db_id: int
    page: int


def results_kb(contests: List[Contest],
               contests_count: int,
               channel_db_id: int,
               page: int = 0):
    kb_obj = InlineKeyboardBuilder()
    for i, contest in enumerate(contests):
        text = unescape(contest.text)
        kb_obj.row(InlineKeyboardButton(text=f'[#{i + 1}] {text[:20] + "..." if len(text) > 15 else text}',
                                        callback_data=ResultsCallback(contest_db_id=contest.id,
                                                                      channel_db_id=channel_db_id,
                                                                      page=page).pack()))
    if page > 0:
        kb_obj.row(
            InlineKeyboardButton(text=f'« {page} стр. ',
                                 callback_data=ResultsChangePageCallback(channel_db_id=channel_db_id,
                                                                         page=page - 1).pack()))
        if contests_count - page * 10 > 10:
            kb_obj.add(
                InlineKeyboardButton(text=f'{page + 2} стр. »',
                                     callback_data=ResultsChangePageCallback(channel_db_id=channel_db_id,
                                                                             page=page + 1).pack()))
    else:
        if contests_count - page * 10 > 10:
            kb_obj.row(
                InlineKeyboardButton(text=f'{page + 2} стр. »',
                                     callback_data=ResultsChangePageCallback(channel_db_id=channel_db_id,
                                                                             page=page + 1).pack()))

    kb_obj.row(InlineKeyboardButton(text='⏪ Отмена',
                                    callback_data=ContestCallback(action="channel_choice",
                                                                  channel_id=channel_db_id).pack()))

    return kb_obj.as_markup()

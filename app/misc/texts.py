from datetime import datetime
from math import ceil
from typing import List

from aiogram.utils.markdown import hbold

from database.models import Channel, Contest
from misc.links import post_link


def make_text_of_created_contests(channel: Channel,
                                  contests: List[Contest]) -> str:
    if not contests:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"

    # TODO: временный (а может и нет ;) ) костыль на ограничение отображения конкурсов - contests[:30]
    channel_contest = list()
    for index, contest in enumerate(contests[:30]):
        additional_text = contest.start_at.strftime(' — Начнется в %H:%M %d.%m.%Y.') \
            if contest.start_at and contest.start_at > datetime.now() else ''
        channel_contest.append(f'{index + 1}) '
                               f'{post_link(contest.channel_tg_id, contest.message_id, "Нажми")}{additional_text}')

    return f"На данный момент в канале {hbold(channel.title)} " \
           f"проходят следующие конкурсы:\n\n" + '\n'.join(channel_contest)


def make_text_of_created_contests_with_pagination(channel: Channel,
                                                  contests: List[Contest],
                                                  contests_count=10,
                                                  page=1) -> str:
    if contests_count <= 0:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"
    elif not contests:
        return f"Перейдите на другую страницу!"

    channel_contest = list()
    for index, contest in enumerate(contests):
        additional_text = contest.start_at.strftime(' — Начнется в %H:%M %d.%m.%Y.') \
            if contest.start_at and contest.start_at > datetime.now() else ''
        channel_contest.append(f'{index + 1}) '
                               f'{post_link(contest.channel_tg_id, contest.message_id, "Нажми")}{additional_text}')

    return f"Конкурсы канала {hbold(channel.title)}:\n" \
           f"{hbold(f'Страница: {page}/{ceil(contests_count / 10)}')}\n\n" + '\n'.join(channel_contest)

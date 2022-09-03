from math import ceil
from typing import List

from aiogram.utils.markdown import hbold

from database.models import Channel, Contest
from misc.links import post_link


def make_list_of_current_contests_text(channel: Channel,
                                       contests: List[Contest]) -> str:
    if not contests:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"

    # TODO: временный (а может и нет ;) ) костыль на ограничение отображения конкурсов - if index < 30
    channel_contest = [f'{index + 1}. {post_link(contest.channel_tg_id, contest.message_id, "Нажми")}'
                       for index, contest in enumerate(contests) if index < 30]
    return f"На данный момент в канале {hbold(channel.title)} " \
           f"проходят следующие конкурсы:\n\n" + '\n'.join(channel_contest)


def make_list_of_current_contests_text_with_pagination(channel: Channel,
                                                       contests: List[Contest],
                                                       contests_count=10,
                                                       page=1) -> str:
    if contests_count <= 0:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"
    elif not contests:
        return f"Перейдите на другую страницу!"

    channel_contest = [f'{index + 1}. {post_link(contest.channel_tg_id, contest.message_id, "Нажми")}'
                       for index, contest in enumerate(contests)]
    return f"Конкурсы канала {hbold(channel.title)}:\n" \
           f"{hbold(f'Страница: {page}/{ceil(contests_count / 10)}')}\n\n" + '\n'.join(channel_contest)

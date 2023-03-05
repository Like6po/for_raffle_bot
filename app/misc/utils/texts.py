from datetime import datetime
from math import ceil
from typing import List

from aiogram.utils.markdown import hbold

from database.contexts import ContestMemberContext
from database.models import Channel, Contest
from misc.utils.links import post_link


def make_text_of_created_contests(channel: Channel,
                                  contests: List[Contest]) -> str:
    if not contests:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"

    # TODO: временный (а может и нет ;) ) костыль на ограничение отображения конкурсов - contests[:30]
    channel_contest = list()
    for index, contest in enumerate(contests[:30]):
        additional_text = contest.start_at.strftime(' — Начнется в %H:%M %d.%m.%Y.') \
            if contest.start_at and contest.start_at > datetime.now() else ''
        link = post_link(contest.channel_tg_id, contest.message_id,
                         contest.text[:27] + "..." if len(contest.text) > 30 else contest.text)
        channel_contest.append(f'{index + 1}) {link}{additional_text}')

    return f"На данный момент в канале {hbold(channel.title)} проходят следующие конкурсы:\n\n" \
        + '\n'.join(channel_contest) \
        + "\n\nЧтобы просмотреть кол-во участников, перейдите в раздел \"Управление Конкурсами\"."


async def make_text_of_created_contests_with_pagination(channel: Channel,
                                                        contests: List[Contest],
                                                        contest_members_db: ContestMemberContext,
                                                        contests_count=10,
                                                        page=1) -> str:
    if contests_count <= 0:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"
    elif not contests:
        return f"Перейдите на другую страницу!"

    channel_contest = list()
    for index, contest in enumerate(contests):
        additional_text = (contest.start_at.strftime(' — Начнется в %H:%M %d.%m.%Y.') if
                           contest.start_at and contest.start_at > datetime.now() else '')

        link = post_link(contest.channel_tg_id, contest.message_id,
                         contest.text[:27] + "..." if len(contest.text) > 30 else contest.text)

        member_count = await contest_members_db.count(contest.id)

        channel_contest.append(f'[#{index + 1}, УЧ: {member_count}] {link}{additional_text}')

    return f"Конкурсы канала {hbold(channel.title)}:\n" \
           f"{hbold(f'Страница: {page}/{ceil(contests_count / 10)}')}\n\n" \
           + '\n'.join(channel_contest) + "\n\nЧтобы завершить конкурс, нажмите на клавиатуре под " \
                                          "этим сообщением кнопку с соответствующим конкурсом."


def make_start_text(fullname: str, alert: str = ''):
    return f'{alert}\n\nПривет, {fullname}!'

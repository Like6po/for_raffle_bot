from typing import List

from aiogram.utils.markdown import hbold

from database.models import Channel, Contest
from misc.links import post_link


def make_list_of_current_contests_text(channel: Channel,
                                       contests: List[Contest]) -> str:
    if not contests:
        return f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!"

    channel_contest = [f'{index + 1}. {post_link(contest.channel_tg_id, contest.message_id, "Нажми")}'
                       for index, contest in enumerate(contests)]
    return f"На данный момент в канале {hbold(channel.title)} проходят следующие конкурсы:\n\n" + '\n'.join(channel_contest)
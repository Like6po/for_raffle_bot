from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from database.contexts.channel import ChannelContext
from database.contexts.contest import ContestContext

from keyboards.contest import contest_action_kb, ContestCallback
from misc.links import post_link


async def contest_channel_choice(cbq: CallbackQuery,
                                 callback_data: ContestCallback,
                                 channel_db: ChannelContext,
                                 contest_db: ContestContext):
    channel = await channel_db.get(channel_id=callback_data.channel_id)
    contests = await contest_db.get_contests_by_channel(channel)

    if not contests:
        await cbq.message.edit_text(f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!",
                                    reply_markup=contest_action_kb(channel.id, contest_results_btn=False))
        return

    channel_contest = [f'{index + 1}. {post_link(contest.tg_id, contest.message_id, "Нажми")}' for index, contest in
                       enumerate(contests)]
    await cbq.message.edit_text(
        f"На данный момент в канале {hbold(channel.title)} проходят следующие конкурсы:\n\n" + '\n'.join(channel_contest),
        reply_markup=contest_action_kb(channel.id))

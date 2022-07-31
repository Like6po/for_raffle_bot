from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from database.contexts.channel import ChannelContext
from database.contexts.contest import ContestContext

from keyboards.contest import contests_kb


async def contest_channel_choice(cbq: CallbackQuery,
                                 channel_db: ChannelContext,
                                 contest_db: ContestContext):
    callback_data = cbq.data.split(":")
    channel = await channel_db.get(channel_id=int(callback_data[3]))
    contests = await contest_db.get_contests_by_channel(channel)

    if not contests:
        await cbq.message.edit_text(f"На данный момент в канале {hbold(channel.title)} не проходят конкурсы!",
                                    reply_markup=contests_kb(contest_results_btn=False))
        return

    channel_contest = [f'{index + 1}. (id{contest.id})' for index, contest in enumerate(contests)]
    await cbq.message.edit_text(
        f"Конкурсы, проходящие сейчас в канале {hbold(channel.title)}:\n\n" + '\n'.join(channel_contest),
        reply_markup=contests_kb())

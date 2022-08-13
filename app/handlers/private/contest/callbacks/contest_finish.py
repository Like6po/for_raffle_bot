from aiogram import Bot
from aiogram.types import CallbackQuery

from database.contexts import ContestMemberContext, MemberContext
from database.contexts.channel import ChannelContext
from database.contexts.contest import ContestContext
from keyboards.results import ResultsCallback
from keyboards.results import results_kb
from misc.contest import choose_the_winners
from misc.texts import make_list_of_current_contests_text


async def contest_finish_cbq(cbq: CallbackQuery,
                             bot: Bot,
                             callback_data: ResultsCallback,
                             contest_db: ContestContext,
                             channel_db: ChannelContext,
                             contest_members_db: ContestMemberContext,
                             member_db: MemberContext):
    await choose_the_winners(bot, contest_db, contest_members_db, member_db, callback_data.contest_db_id)

    await cbq.message.edit_text(
        make_list_of_current_contests_text(await channel_db.get(channel_id=callback_data.channel_db_id),
                                           await contest_db.get_all(callback_data.channel_db_id)),
        reply_markup=results_kb(await contest_db.get_all(callback_data.channel_db_id), callback_data.channel_db_id)
    )

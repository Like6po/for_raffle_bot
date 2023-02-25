from aiogram.types import CallbackQuery

from database.contexts.channel import ChannelContext
from database.contexts.contest import ContestContext
from keyboards.contest import contest_action_kb, ContestCallback
from misc.utils.texts import make_text_of_created_contests


async def contest_channel_choice(cbq: CallbackQuery,
                                 callback_data: ContestCallback,
                                 channel_db: ChannelContext,
                                 contest_db: ContestContext):
    await cbq.message.edit_text(
        make_text_of_created_contests(chnl := await channel_db.get(channel_id=callback_data.channel_id),
                                      await contest_db.get_all_active(callback_data.channel_id)),
        reply_markup=contest_action_kb(chnl.id)
    )
    await cbq.answer()

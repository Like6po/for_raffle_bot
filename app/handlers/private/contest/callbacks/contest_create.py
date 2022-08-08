from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from states.contest import ContestStatus
from keyboards.contest import contest_kb, ContestCallback


async def contest_create(cbq: CallbackQuery, state: FSMContext):
    callback_data = ContestCallback.unpack(cbq.data)
    await state.clear()
    await state.update_data({
        'channel_id': callback_data.channel_id
    })
    await state.set_state(ContestStatus.text)

    await cbq.message.edit_text("📋 Напиши текст для поста!", reply_markup=contest_kb(callback_data.channel_id))

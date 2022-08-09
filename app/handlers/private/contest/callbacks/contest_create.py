from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.contest import contest_kb, ContestCallback
from states.contest import ContestStatus


async def contest_create(cbq: CallbackQuery,
                         callback_data: ContestCallback,
                         state: FSMContext):
    await state.clear()
    await state.update_data({
        'channel_id': callback_data.channel_id
    })
    await state.set_state(ContestStatus.text)

    await cbq.message.edit_text("📋 Напиши текст для поста!", reply_markup=contest_kb(callback_data.channel_id))

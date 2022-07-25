from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from states.user import UserStatus
from keyboards.start import start_kb


async def channels_back(cbq: CallbackQuery, bot: Bot):
    await cbq.message.edit_text(text=f'Привет, {cbq.from_user.full_name}!')
    await cbq.message.edit_reply_markup(reply_markup=start_kb())
    await bot.answer_callback_query(cbq.id)


async def channels_add(cbq: CallbackQuery, state: FSMContext, bot: Bot):
    await cbq.message.answer("Отправьте мне юзернейм канала или перешлите сообщение оттуда!")
    await state.set_state(UserStatus.wait_channel_message)
    await bot.answer_callback_query(cbq.id)
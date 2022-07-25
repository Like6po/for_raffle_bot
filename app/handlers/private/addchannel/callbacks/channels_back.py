from aiogram.types import CallbackQuery

from keyboards.start import start_kb


async def channels_back(cbq: CallbackQuery):
    await cbq.message.edit_text(text=f'Привет, {cbq.from_user.full_name}!',
                                reply_markup=start_kb())

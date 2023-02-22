from aiogram.types import CallbackQuery

from keyboards.start import start_kb
from misc.utils.texts import make_start_text


async def channels_back(cbq: CallbackQuery):
    await cbq.message.edit_text(text=make_start_text(cbq.from_user.full_name),
                                reply_markup=start_kb())

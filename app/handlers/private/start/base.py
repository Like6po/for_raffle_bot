from aiogram.types import Message

from database.contexts.user import UserContext
from keyboards.start import start_kb
from misc.utils.texts import make_start_text


async def command_start(message: Message,
                        user_db: UserContext):
    await user_db.get_or_create_and_get(message.from_user)
    await message.answer(text=make_start_text(message.from_user.full_name),
                         reply_markup=start_kb())

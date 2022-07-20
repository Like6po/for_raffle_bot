from aiogram.types import Message

from database.contexts.user import UserContext
from keyboards.start import start_kb


async def command_start(message: Message,
                        user_db: UserContext):
    user = await user_db.get_or_create_and_get(message.from_user)

    await message.answer(text=f'Привет, {user.full_name}! Ваш id = {user.id}',
                         reply_markup=start_kb())

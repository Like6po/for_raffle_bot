from aiogram.types import Message

from keyboards.start import start_kb


async def command_start(message: Message):
    await message.answer(text=f'Привет, мир!',
                         reply_markup=start_kb())

from aiogram.types import CallbackQuery

from keyboards.contest import ContestCallback


async def contest_join(cbq: CallbackQuery):
    print(f"Получено нажатие на кнопку участия в конкурсе в канале {cbq.message.chat.title}!")

from aiogram.types import CallbackQuery


async def post_preview_cbq(cbq: CallbackQuery):
    return await cbq.answer('Это лишь превью поста.', cache_time=300)

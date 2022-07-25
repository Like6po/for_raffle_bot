from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from states.user import UserStatus


async def command_addchannel(message: Message, state: FSMContext):
    await message.answer("Отправьте мне юзернейм канала или перешлите сообщение оттуда!")
    await state.set_state(UserStatus.wait_channel_message)

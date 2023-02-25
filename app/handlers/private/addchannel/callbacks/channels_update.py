from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.channels import channels_cancel_kb
from states.user import UserStatus


async def channels_update(cbq: CallbackQuery,
                          state: FSMContext):
    await state.set_state(UserStatus.wait_channel_message_to_update)
    await cbq.message.edit_text(text="Отправьте мне юзернейм канала или перешлите сообщение оттуда!",
                                reply_markup=channels_cancel_kb())

from aiogram.dispatcher.fsm.state import State, StatesGroup


class UserStatus(StatesGroup):
    wait_channel_message = State()
    wait_channel_message_to_update = State()

from aiogram.dispatcher.fsm.state import State, StatesGroup


class ContestStatus(StatesGroup):
    channel_id = State()
    text = State()
    btn_title = State()
    attachment_hash = State()
    is_attachment_preview = State()
    winner_count = State()
    sponsor_channels = State()
    start_at = State()
    end_at = State()
    end_count = State()

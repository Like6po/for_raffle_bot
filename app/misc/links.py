from aiogram.types.chat import Chat as AiogramChat
from aiogram.types.user import User as AiogramUser
from aiogram.utils.markdown import hlink


def user_link(user=None, title: str = None, full_name=None, tg_id=None, username=None, is_force_by_id=False):
    full_name = user.full_name if user else full_name
    tg_id = user.id if (user and isinstance(user, AiogramUser)) else user.tg_id if user else tg_id
    username = user.username if user else username

    return hlink(title if title else full_name if full_name else "no_name",
                 f"t.me/{username}" if username and not is_force_by_id else f"tg://openmessage?user_id={tg_id}")


def chat_link(chat: AiogramChat = None, username=None, tg_id=None, title=None):
    username = chat.username if chat else username
    tg_id = chat.id if chat else tg_id
    title = chat.title if chat else title

    return hlink(title,
                 f"t.me/{username}" if username else f"tg://openmessage?chat_id={((tg_id * -1) - 1000000000000) if tg_id < -1000000000000 else tg_id}")


def post_link(chat_id: int = None, message_id: int = None, title: str = None):
    return hlink(title,
                 f"t.me/c/{((chat_id * -1) - 1000000000000) if chat_id < -1000000000000 else chat_id}/{message_id}")

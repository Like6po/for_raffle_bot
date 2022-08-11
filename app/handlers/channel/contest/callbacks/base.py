from aiogram.types import CallbackQuery

from database import MemberContext
from keyboards.contest import JoinButtonCallback


async def contest_join(cbq: CallbackQuery,
                       callback_data: JoinButtonCallback,
                       member_db: MemberContext):
    if not await member_db.exists(callback_data.contest_db_id, cbq.from_user):
        await member_db.new(callback_data.contest_db_id, cbq.from_user)
        return await cbq.answer('Вы успешно зарегались.', show_alert=True)

    else:
        await member_db.delete(callback_data.contest_db_id, cbq.from_user)
        return await cbq.answer('Вы успешно самоудалились из конкурса, молодцы.', show_alert=True)

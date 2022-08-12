from aiogram import Bot
from aiogram.types import CallbackQuery

from database.contexts import MemberContext, ContestContext, ContestMemberContext
from keyboards.contest import JoinButtonCallback
from misc.contest import is_channel_member


async def contest_join(cbq: CallbackQuery,
                       bot: Bot,
                       callback_data: JoinButtonCallback,
                       contest_db: ContestContext,
                       member_db: MemberContext,
                       contest_members_db: ContestMemberContext):
    member_data = await member_db.get_or_create_and_get(cbq.from_user)
    contest_data = await contest_db.get_by_db_id(callback_data.contest_db_id)

    if not is_channel_member(await bot.get_chat_member(contest_data.channel_tg_id, cbq.from_user.id)):
        return await cbq.answer('Для начала подпишитесь на этот канал!', show_alert=True)

    if not await contest_members_db.exists(callback_data.contest_db_id, member_data.id):
        await contest_members_db.add(callback_data.contest_db_id, member_data.id)
        await cbq.answer('Вы успешно зарегались.', show_alert=True)

        if contest_data.end_count:
            if contest_data.end_count <= await contest_members_db.count(callback_data.contest_db_id):
                pass  # TODO: завершить конкурс

    else:
        await contest_members_db.delete(callback_data.contest_db_id, member_data.id)
        return await cbq.answer('Вы успешно самоудалились из конкурса, молодцы.', show_alert=True)

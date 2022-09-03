from aiogram import Bot
from aiogram import html
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from database.contexts import MemberContext, ContestContext, ContestMemberContext, ChannelContext
from keyboards.contest import JoinButtonCallback
from misc.contest import is_channel_member


async def contest_join(cbq: CallbackQuery,
                       bot: Bot,
                       callback_data: JoinButtonCallback,
                       channel_db: ChannelContext,
                       contest_db: ContestContext,
                       member_db: MemberContext,
                       contest_members_db: ContestMemberContext):
    member_data = await member_db.get_or_create_and_get(cbq.from_user)
    contest_data = await contest_db.get_by_db_id(callback_data.contest_db_id)

    if contest_data.sponsor_channels:
        if not is_channel_member(await bot.get_chat_member(contest_data.channel_tg_id, cbq.from_user.id)):
            return await cbq.answer('Для начала подпишитесь на этот канал!', show_alert=True)

        for channel_id in contest_data.sponsor_channels:
            if not is_channel_member(await bot.get_chat_member(channel_id, cbq.from_user.id)):
                return await cbq.answer(f'Вы не подписаны на '
                                        f'{html.quote((await channel_db.get(tg_id=channel_id)).title)}!', show_alert=True)

    if not await contest_members_db.exists(callback_data.contest_db_id, member_data.id):
        return await cbq.answer(url=await create_start_link(bot=bot,
                                                            payload=f"join-contest_{callback_data.contest_db_id}",
                                                            encode=True))
    else:
        await contest_members_db.delete(callback_data.contest_db_id, member_data.id)
        return await cbq.answer('Вы больше не учавствуете в конкурсе!', show_alert=True)

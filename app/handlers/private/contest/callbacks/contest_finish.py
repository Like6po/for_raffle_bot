from aiogram import Bot
from aiogram.types import CallbackQuery

from database.contexts import ContestMemberContext, MemberContext
from database.contexts.channel import ChannelContext
from database.contexts.contest import ContestContext
from keyboards.results import ResultsCallback
from keyboards.results import results_kb
from misc.contest import choose_the_winners
from misc.texts import make_list_of_current_contests_text


async def contest_finish_cbq(cbq: CallbackQuery,
                             bot: Bot,
                             callback_data: ResultsCallback,
                             contest_db: ContestContext,
                             channel_db: ChannelContext,
                             contest_members_db: ContestMemberContext,
                             member_db: MemberContext):
    winners_list = await choose_the_winners(contest_db, contest_members_db, member_db, callback_data.contest_db_id)

    if len(winners_list) <= 0:
        return await cbq.message.edit_text('Не могу выбрать победителя! Никто не учавствует!',
                                           reply_markup=results_kb(
                                               await contest_db.get_all(callback_data.channel_db_id),
                                               callback_data.channel_db_id))

    string = f'Конкурс завершён! Спасибо за участие!\n\nСписок победителей:\n' + \
             '\n'.join(f'{i + 1}) {user_link(title=user.full_name, tg_id=user.tg_id)}'
                       for i, user in enumerate(winners_list))

    msg = await bot.send_message(contest_data.channel_tg_id, string, reply_to_message_id=contest_data.message_id)
    link_to_post = post_link(contest_data.channel_tg_id, msg.message_id)

    if contest_data.attachment_hash:
        await bot.edit_message_caption(contest_data.channel_tg_id,
                                       contest_data.message_id,
                                       caption=contest_data.text + f'\n\nПобедители: {link_to_post}')
    else:
        await bot.edit_message_text(contest_data.text + f'\n\nПобедители: {link_to_post}',
                                    contest_data.channel_tg_id,
                                    contest_data.message_id)

    await cbq.message.edit_text(
        make_list_of_current_contests_text(await channel_db.get(channel_id=callback_data.channel_db_id),
                                           await contest_db.get_all(callback_data.channel_db_id)),
        reply_markup=results_kb(await contest_db.get_all(callback_data.channel_db_id), callback_data.channel_db_id)
    )

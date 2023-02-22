from aiogram import Bot
from aiogram.dispatcher.filters import CommandObject
from aiogram.types import Message

from database.contexts import ContestContext, ContestMemberContext, MemberContext
from misc.utils.contest import choose_the_winners


async def command_start_deeplink(message: Message,
                                 command: CommandObject,
                                 bot: Bot,
                                 contest_db: ContestContext,
                                 contest_members_db: ContestMemberContext,
                                 member_db: MemberContext):
    try:
        deeplink_name, arg2 = command.args.split('_', maxsplit=1)
    except ValueError:
        return await message.answer(text=f'Ошибка. Пожайлуста, не играйтесь с диплинком ;)')

    if deeplink_name == 'join-contest':  # пример использования: handlers/channel/contest/callbacks/base.py, 23 line
        contest_db_id = int(arg2)

        member_data = await member_db.get_or_create_and_get(message.from_user)
        contest_data = await contest_db.get_by_db_id(contest_db_id)

        await contest_members_db.add(contest_db_id, member_data.id)
        await message.reply('Вы успешно зарегистрировались.')

        if contest_data.end_count:
            if contest_data.end_count <= await contest_members_db.count(contest_db_id):
                await choose_the_winners(bot, contest_db, contest_members_db, member_db, contest_db_id)

    # elif deeplink_name == 'еще какие-нибудь диплинки':
    else:
        return await message.answer(text=f'Ошибка. Такого диплинка не существует.')

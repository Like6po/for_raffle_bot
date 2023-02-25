from datetime import datetime
from random import choice
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMember
from aiogram.utils.markdown import hbold

from database.contexts import ContestContext, ContestMemberContext, MemberContext, ChannelContext
from database.models import Member, ContestMember, Contest
from keyboards.results import post_button_with_results
from misc.config import config
from misc.utils.links import user_link
from misc.utils.telegraph_api import create_page_with_winners


class InvalidContentError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__()

    def __str__(self):
        return self.reason


async def get_content(message: Message,
                      last_state: str,
                      bot: Bot = None,
                      channel_db: ChannelContext = None):
    if last_state == 'text':
        return message.html_text

    elif last_state == 'btn_title':
        return message.text

    elif last_state == 'attachment_hash':
        if message.photo:
            return f"{message.photo[-1].file_id}:photo"
        if message.document:
            return f"{message.document.file_id}:document"
        if message.video:
            return f"{message.video.file_id}:video"
        return InvalidContentError('Принимается фото, видео, либо документ!')

    elif last_state == 'sponsor_channels':
        if message.text.lower() == 'закончить':
            return True

        channel_ids_set = set()

        # если переслано сообщение из канала
        if message.forward_from_chat:
            channel_ids_set.add((await channel_db.get(message.forward_from_chat)).tg_id)
            return channel_ids_set

        # если условие выше не выполнено (т.е юзернеймы каналов в тексте)
        try:
            channels_list = message.text.split(' ')
        except ValueError:
            channels_list = [message.text]

        for channel_username in channels_list:
            if not channel_username.startswith('@'):
                return InvalidContentError('Пожалуйста, пришлите либо юзернейм канала, '
                                           'либо пересланное с канала сообщение!')
            try:
                channel = await channel_db.get(await bot.get_chat(channel_username))
                if not channel:
                    return InvalidContentError('Такого канала нет в базе данных!')
                channel_ids_set.add(channel.tg_id)
            except TelegramBadRequest as e:
                if e.message.startswith('Bad Request: chat not found'):
                    return InvalidContentError('Такого канала не существует, либо он не зарегистрирован!')

        return channel_ids_set

    elif last_state in ['winner_count', 'end_count']:
        try:
            return int(message.text)
        except:
            return InvalidContentError('Пожалуйста, отправьте число!')

    elif last_state in ['start_at', 'end_at']:
        try:
            return datetime.strptime(message.text, '%H:%M %d.%m.%Y').isoformat()
        except:
            return None


async def send_post(bot: Bot,
                    chat_id: int,
                    state_data: dict,
                    reply_markup=None,
                    is_contest_start=False,
                    contest_db: ContestContext = None,
                    contest_data: Contest = None) -> None:
    msg = None

    if not state_data['attachment_hash']:
        msg = await bot.send_message(chat_id=chat_id, text=state_data['text'], parse_mode='HTML',
                                     reply_markup=reply_markup)
        if is_contest_start:
            await contest_db.set_message_id(contest_data.id, msg.message_id)
        return

    file_type = state_data['attachment_hash'].split(':')[-1]
    if file_type == 'photo':
        msg = await bot.send_photo(chat_id=chat_id, photo=state_data['attachment_hash'].split(':')[0],
                                   caption=state_data['text'],
                                   reply_markup=reply_markup)

    elif file_type == 'document':
        msg = await bot.send_document(chat_id=chat_id, document=state_data['attachment_hash'].split(':')[0],
                                      caption=state_data['text'],
                                      reply_markup=reply_markup)

    elif file_type == 'video':
        msg = await bot.send_video(chat_id=chat_id, video=state_data['attachment_hash'].split(':')[0],
                                   caption=state_data['text'],
                                   reply_markup=reply_markup)

    if is_contest_start:
        await contest_db.set_message_id(contest_data.id, msg.message_id)


def is_channel_member(chat_member: ChatMember):
    return isinstance(chat_member, (ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember))


async def choose_the_winners(bot: Bot,
                             contest_db: ContestContext,
                             contest_members_db: ContestMemberContext,
                             member_db: MemberContext,
                             contest_db_id: int):
    contest_data = await contest_db.get_by_db_id(contest_db_id)
    contest_members_list = await contest_members_db.get_all(contest_db_id)

    if not contest_data:
        return

    string = contest_data.start_at.astimezone(config.timezone).strftime('• Начался в %H:%M %d.%m.%Y МСК.\n') \
        if contest_data.start_at \
        else contest_data.created_at.astimezone(config.timezone).strftime('• Начался в %H:%M %d.%m.%Y МСК.\n')

    string += datetime.now(config.timezone).strftime('• Закончился в %H:%M %d.%m.%Y МСК.\n')

    string += f'• Количество участников: {len(contest_members_list)}\n'
    string += f'• Количество победителей: {contest_data.winner_count}\n\n'
    string += f'{hbold("Список Победителей:")}\n'

    if not len(contest_members_list) <= 0:
        winners_list: List[Member | ContestMember] = list()

        members_count = len(contest_members_list)
        # щас winners_list это список ContestMember
        for index in range(0, contest_data.winner_count):
            if index <= members_count - 1:  # если кол-во участников < кол-во победителей
                winner = choice(contest_members_list)
                winners_list.append(winner)
                contest_members_list.remove(winner)

        # а тут превращается в список Member
        for index, winner in enumerate(winners_list):
            winners_list[index] = await member_db.get(db_id=winner.member_db_id)

        string += '\n'.join(f'{i + 1}) {user_link(title=user.full_name, tg_id=user.tg_id)}'
                            for i, user in enumerate(winners_list))
    else:
        string += 'Победители отсутствуют.'

    await bot.edit_message_reply_markup(contest_data.channel_tg_id,
                                        contest_data.message_id,
                                        reply_markup=post_button_with_results(await create_page_with_winners(string)))

    await contest_db.finish(contest_db_id)
    await contest_members_db.finish_contest(contest_db_id)

    if contest_data.is_notify_contest_end:
        await bot.send_message(contest_data.channel_tg_id,
                               '🎉 Конкурс был завершен!',
                               reply_to_message_id=contest_data.message_id)


# async def add_channel_if_not_exists(channel: Chat, channel_db: ChannelContext):
#     if await channel_db.exists(Channel.tg_id == channel.id):
#         return
#     await channel_db.add(title=channel.title, tg_id=channel.id, username=channel.username)

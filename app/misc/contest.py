from datetime import datetime
from random import choice
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMember

from database.contexts import ContestContext, ContestMemberContext, MemberContext, ChannelContext
from database.models import Member, ContestMember
from misc.links import post_link, user_link


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
        return None

    elif last_state == 'sponsor_channels':
        channel_ids_set = set()

        # если переслано сообщение из канала
        if message.forward_from_chat:
            channel = await channel_db.get(message.forward_from_chat)
            if channel:
                channel_ids_set.add(channel.tg_id)
                return channel_ids_set
            else:
                return

        if message.text.lower() == 'закончить':
            return True

        # если условие выше не выполнено (т.е юзернеймы каналов в тексте)
        try:
            channels_list = message.text.split(' ')
        except ValueError:
            channels_list = [message.text]

        for channel_username in channels_list:
            if not channel_username.startswith('@'):
                return
            try:
                channel = await channel_db.get(await bot.get_chat(channel_username))
                if not channel:
                    return
                channel_ids_set.add(channel.tg_id)
            except TelegramBadRequest as e:
                if e.message.startswith('Bad Request: chat not found'):
                    return

        return channel_ids_set

    elif last_state in ['winner_count', 'end_count']:
        try:
            return int(message.text)
        except:
            return None

    elif last_state in ['start_at', 'end_at']:
        try:
            return datetime.strptime(message.text, '%H:%M %d.%m.%Y')
        except:
            return None


async def send_post(bot: Bot, chat_id: int, state_data: dict, reply_markup=None) -> Message:
    if not state_data['attachment_hash']:
        return await bot.send_message(chat_id=chat_id, text=state_data['text'], parse_mode='HTML',
                                      reply_markup=reply_markup,
                                      disable_web_page_preview=state_data['is_attachment_preview'])

    file_type = state_data['attachment_hash'].split(':')[-1]
    if file_type == 'photo':
        return await bot.send_photo(chat_id=chat_id, photo=state_data['attachment_hash'].split(':')[0],
                                    caption=state_data['text'],
                                    parse_mode='HTML', reply_markup=reply_markup)

    elif file_type == 'document':
        return await bot.send_document(chat_id=chat_id, document=state_data['attachment_hash'].split(':')[0],
                                       caption=state_data['text'],
                                       parse_mode='HTML', reply_markup=reply_markup)


def is_channel_member(chat_member: ChatMember):
    return isinstance(chat_member, (ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember))


async def choose_the_winners(contest_db: ContestContext,
                             contest_members_db: ContestMemberContext,
                             member_db: MemberContext,
                             contest_db_id: int):
    contest_data = await contest_db.get_by_db_id(contest_db_id)
    contest_members_list = await contest_members_db.get_all(contest_db_id)

    winners_list: List[Member | ContestMember] = list()

    # щас winners_list это список ContestMember
    for _ in range(0, contest_data.winner_count):
        if len(contest_members_list) <= 0:
            break
        winner = choice(contest_members_list)
        winners_list.append(winner)
        contest_members_list.remove(winner)

    # а тут превращается в список Member
    for index, winner in enumerate(winners_list):
        winners_list[index] = await member_db.get(db_id=winner.member_db_id)

    if len(winners_list) > 0:
        await contest_db.finish(contest_db_id)
        await contest_members_db.finish_contest(contest_db_id)

    return winners_list

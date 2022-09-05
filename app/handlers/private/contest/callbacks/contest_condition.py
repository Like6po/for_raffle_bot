from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from database.contexts import ChannelContext, ContestContext
from keyboards.contest import contest_kb, post_button_kb, ContestCallback
from misc.config import config
from misc.contest import send_post
from scheduled.close_contest import close_contest
from scheduled.start_contest import start_contest
from states.contest import ContestStatus


async def contest_condition(cbq: CallbackQuery,
                            bot: Bot,
                            callback_data: ContestCallback,
                            state: FSMContext,
                            channel_db: ChannelContext,
                            contest_db: ContestContext,
                            bot_pickle,
                            scheduler: AsyncIOScheduler):
    state_data = await state.get_data()

    if not state_data.get('channel_id', None):
        return await cbq.message.reply('Ой-ой! channel_id был утерян!\nplaceholder: /start ')

    if callback_data.last_state == 'text':
        if callback_data.condition:
            await state.set_state(ContestStatus.btn_title)
            await cbq.message.edit_text('Теперь укажите название для кнопки!',
                                        reply_markup=contest_kb(callback_data.channel_id, last_state='btn_title'))
        else:
            state_data.update({
                'btn_title': None
            })
            await cbq.message.edit_text('🖼 Отлично, как насчёт вложений?',
                                        reply_markup=contest_kb(state_data['channel_id'],
                                                                last_state='btn_title',
                                                                condition_buttons_title=(
                                                                    '✅ С вложением', '❌ Без вложения')))

    elif callback_data.last_state == 'btn_title':
        if callback_data.condition:
            await state.set_state(ContestStatus.attachment_hash)
            await cbq.message.edit_text(
                'Отправьте мне вложение!\nПримечание: поддерживаются только документы и фотографии.',
                reply_markup=contest_kb(callback_data.channel_id, last_state='attachment_hash'))
        else:
            state_data.update({
                'attachment_hash': None
            })
            await state.set_state(ContestStatus.is_notify_contest_end)
            await cbq.message.edit_text('Пост об окончании конкурса',
                                        reply_markup=contest_kb(callback_data.channel_id,
                                                                last_state='attachment_hash',
                                                                condition_buttons_title=('✅ Включить', '❌ Отключить')))

    elif callback_data.last_state == 'attachment_hash':
        state_data.update({
            'is_notify_contest_end': callback_data.condition
        })

        await state.set_state(ContestStatus.winner_count)
        await cbq.message.edit_text('👥 Укажите количество победителей!',
                                    reply_markup=contest_kb(callback_data.channel_id,
                                                            last_state='is_notify_contest_end'))

    elif callback_data.last_state == 'winner_count':
        if callback_data.condition:
            state_data.update({
                'sponsor_channels': None
            })
            await cbq.message.edit_text(
                '📅 Когда опубликуем пост?',
                reply_markup=contest_kb(callback_data.channel_id, last_state='sponsor_channels',
                                        condition_buttons_title=('🔜 Сразу', '📆 В определённую дату')))
        else:
            await state.set_state(ContestStatus.sponsor_channels)
            await cbq.message.edit_text(
                f'Укажите юзернеймы каналов через пробел или перешлите сообщение из канала.'
                f'ex: @danya @dane4ka @danil',
                reply_markup=contest_kb(callback_data.channel_id, last_state='sponsor_channels'))

    elif callback_data.last_state == 'sponsor_channels':
        if callback_data.condition:
            state_data.update({
                'start_at': None
            })
            await cbq.message.edit_text(
                '⛔ Конкурс будет закончен в определённую дату или при достижении нужного количества участников?',
                reply_markup=contest_kb(callback_data.channel_id, last_state='start_at',
                                        condition_buttons_title=('👤 Учаcтники', '📆 Дата')))
        else:
            await state.set_state(ContestStatus.start_at)
            await cbq.message.edit_text(
                f'Отправь мне дату публикации поста!\nФормат: {hbold("часы:минуты день.месяц.год")}\n'
                f'Пример: {hbold("18:03 08.09.2022")}',
                reply_markup=contest_kb(callback_data.channel_id, last_state='start_at'))

    elif callback_data.last_state == 'start_at':
        if callback_data.condition:
            await state.set_state(ContestStatus.end_count)
            await cbq.message.edit_text('Укажите количество участников для окончания конкурса!',
                                        reply_markup=contest_kb(callback_data.channel_id, last_state='end_count'))
        else:
            await state.set_state(ContestStatus.end_at)
            await cbq.message.edit_text(
                f'Отправь мне дату окончания конкурса!\nФормат: {hbold("часы:минуты день.месяц.год")}\n'
                f'Пример: {hbold("18:03 08.09.2022")}',
                reply_markup=contest_kb(callback_data.channel_id, last_state='end_at'))

    elif callback_data.last_state in ['end_count', 'end_at']:
        await state.clear()

        state_data['start_at'] = datetime.fromisoformat(state_data['start_at']) if state_data['start_at'] else None
        state_data['end_at'] = datetime.fromisoformat(state_data['end_at']) if state_data['end_at'] else None

        channel_data = await channel_db.get(channel_id=state_data['channel_id'])
        contest_data = await contest_db.new(user=cbq.from_user,
                                            channel=channel_data,
                                            channel_tg_id=channel_data.tg_id,
                                            text=state_data['text'],
                                            btn_title=state_data['btn_title'],
                                            winner_count=state_data['winner_count'],
                                            attachment_hash=state_data['attachment_hash'],
                                            start_at=state_data['start_at'],
                                            end_at=state_data['end_at'],
                                            end_count=state_data['end_count'],
                                            sponsor_channels=state_data['sponsor_channels'],
                                            is_notify_contest_end=state_data['is_notify_contest_end'])

        if state_data['start_at']:
            scheduler.add_job(start_contest, args=[bot_pickle, channel_data, contest_data, state_data],
                              trigger=IntervalTrigger(start_date=state_data['start_at'],
                                                      end_date=state_data['start_at'] + timedelta(seconds=5),
                                                      timezone=config.timezone),
                              max_instances=1, id=f'start_contest_{contest_data.id}', misfire_grace_time=3)
            if state_data['end_at']:
                secs = (state_data['end_at'] - state_data['start_at']).total_seconds()
                scheduler.add_job(close_contest, args=[bot_pickle, contest_data],
                                  trigger=IntervalTrigger(start_date=state_data['start_at'] + timedelta(seconds=secs),
                                                          end_date=state_data['start_at'] + timedelta(seconds=secs + 5),
                                                          timezone=config.timezone),
                                  max_instances=1, id=f'close_contest_{contest_data.id}', misfire_grace_time=3)
            return await cbq.message.edit_text('todo: succesfully added job')

        elif state_data['end_at']:
            scheduler.add_job(close_contest, args=[bot_pickle, contest_data],
                              trigger=IntervalTrigger(start_date=state_data['end_at'],
                                                      end_date=state_data['end_at'] + timedelta(seconds=5),
                                                      timezone=config.timezone),
                              max_instances=1, id=f'close_contest_{contest_data.id}', misfire_grace_time=3)

        await send_post(bot, channel_data.tg_id, state_data, post_button_kb(state_data['btn_title'], contest_data.id),
                        True, contest_db, contest_data)

        return await cbq.message.edit_text('todo: finish text + keyboard')

    await state.update_data(state_data)

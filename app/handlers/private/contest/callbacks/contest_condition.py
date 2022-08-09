from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from keyboards.contest import contest_kb, ContestCallback
from states.contest import ContestStatus


async def contest_condition(cbq: CallbackQuery,
                            callback_data: ContestCallback,
                            state: FSMContext):
    state_data = await state.get_data()
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
            await state.set_state(ContestStatus.is_attachment_preview)
            await cbq.message.edit_text('🌐 Предпросмотр ссылок',
                                        reply_markup=contest_kb(callback_data.channel_id,
                                                                last_state='attachment_hash',
                                                                condition_buttons_title=('✅ Включить', '❌ Отключить')))

    elif callback_data.last_state == 'attachment_hash':
        state_data.update({
            'is_attachment_preview': callback_data.condition
        })

        await state.set_state(ContestStatus.winner_count)
        await cbq.message.edit_text('👥 Укажите количество победителей!',
                                    reply_markup=contest_kb(callback_data.channel_id,
                                                            last_state='is_attachment_preview'))

    elif callback_data.last_state == 'winner_count':
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
                f'Отправь мне дату публикации поста!\nФормат: {hbold("часы:минуты день.месяц.год")}\nПример: {hbold("18:03 08.09.2022")}',
                reply_markup=contest_kb(callback_data.channel_id, last_state='start_at'))

    elif callback_data.last_state == 'start_at':
        if callback_data.condition:
            await state.set_state(ContestStatus.end_count)
            await cbq.message.edit_text('Укажите количество участников для окончания конкурса!',
                                        reply_markup=contest_kb(callback_data.channel_id, last_state='end_count'))
        else:
            await state.set_state(ContestStatus.end_at)
            await cbq.message.edit_text(
                f'Отправь мне дату окончания конкурса!\nФормат: {hbold("часы:минуты день.месяц.год")}\nПример: {hbold("18:03 08.09.2022")}',
                reply_markup=contest_kb(callback_data.channel_id, last_state='end_at'))

    await state.update_data(state_data)

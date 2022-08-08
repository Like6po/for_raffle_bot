from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from states.contest import ContestStatus
from keyboards.contest import contest_kb, ContestCallback


async def contest_return(cbq: CallbackQuery, state: FSMContext):
    callback_data = ContestCallback.unpack(cbq.data)
    await state.set_state('ContestStatus:' + callback_data.last_state)

    if callback_data.last_state == 'text':
        await cbq.message.edit_text("📋 Напиши текст для поста!", reply_markup=contest_kb(callback_data.channel_id))

    elif callback_data.last_state == 'btn_title':
        await cbq.message.edit_text(
            '🔘 Хорошо, будем указывать название для кнопки или оставим по умолчанию? (По умолчанию: "Учавствовать")',
            reply_markup=contest_kb(callback_data.channel_id,
                                    last_state='text',
                                    condition_buttons_title=('📔 Указать', '🔜 По умолчанию')))

    elif callback_data.last_state == 'attachment_hash':
        await cbq.message.edit_text('🖼 Отлично, как насчёт вложений?',
                                    reply_markup=contest_kb(callback_data.channel_id,
                                                            last_state='btn_title',
                                                            condition_buttons_title=('✅ С вложением', '❌ Без вложения')))
    elif callback_data.last_state == 'is_attachment_preview':
        await cbq.message.edit_text('🌐 Предпросмотр ссылок',
                                    reply_markup=contest_kb(callback_data.channel_id,
                                                            last_state='attachment_hash',
                                                            condition_buttons_title=('✅ Включить', '❌ Отключить')))

    elif callback_data.last_state == 'winner_count':
        await cbq.message.edit_text('👥 Укажите количество победителей!',
                                    reply_markup=contest_kb(callback_data.channel_id,
                                                            last_state='is_attachment_preview'))

    elif callback_data.last_state == 'start_at':
        await state.set_state()
        await cbq.message.edit_text('📅 Когда опубликуем пост?',
                                    reply_markup=contest_kb(callback_data.channel_id, last_state='winner_count',
                                                            condition_buttons_title=('🔜 Сразу', '📆 В определённую дату')))

    elif callback_data.last_state in ['end_at', 'end_count']:
        await state.set_state()
        await cbq.message.edit_text(
            '⛔ Конкурс будет закончен в определённую дату или при достижении нужного количества участников?',
            reply_markup=contest_kb(callback_data.channel_id, last_state='start_at',
                                    condition_buttons_title=('👤 Учаcтники', '📆 Дата')))

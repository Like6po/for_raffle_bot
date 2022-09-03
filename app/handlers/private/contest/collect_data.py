from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode

from database.contexts import ChannelContext
from keyboards.contest import contest_kb, post_button_kb
from misc.contest import get_content, send_post
from misc.links import chat_link


async def collect_data(message: Message,
                       state: FSMContext,
                       bot: Bot,
                       channel_db: ChannelContext):
    state_data = await state.get_data()
    last_state = (await state.get_state()).split(':')[-1]

    if not state_data.get('channel_id', None):
        return await message.reply('Ой-ой! channel_id был утерян!\nplaceholder: /start ')

    if content := await get_content(message, last_state, bot, channel_db):
        if last_state in ['end_count', 'end_at']:
            state_data.update({
                'end_count' if last_state == 'end_at' else 'end_at': None
            })

        if last_state == 'sponsor_channels':
            if content is not True:
                ids_set = state_data.get(last_state, set())
                if ids_set is None:  # если использовать "назад"
                    ids_set = set()
                ids_set.update(content)
                state_data.update({last_state: ids_set})
            else:  # если сразу написать Закончить
                if not state_data.get(last_state, None):
                    state_data.update({last_state: None})
        else:
            state_data.update({
                last_state: content
            })
        await state.update_data(state_data)
        # print(f'{last_state}: {state_data}')
    else:
        await message.answer('Структура сообщения не верна или контент не найден в базе данных!')
        return

    if last_state == 'text':
        await state.set_state()
        await message.answer(
            '🔘 Хорошо, будем указывать название для кнопки или оставим по умолчанию? (По умолчанию: "Учавствовать")',
            reply_markup=contest_kb(state_data['channel_id'],
                                    last_state=last_state,
                                    condition_buttons_title=('📔 Указать', '🔜 По умолчанию')))
    elif last_state == 'btn_title':
        await state.set_state()
        await message.answer('🖼 Отлично, как насчёт вложений?',
                             reply_markup=contest_kb(state_data['channel_id'],
                                                     last_state=last_state,
                                                     condition_buttons_title=('✅ С вложением', '❌ Без вложения')))

    elif last_state == 'attachment_hash':
        await state.set_state()
        await message.answer('🌐 Предпросмотр ссылок',
                             reply_markup=contest_kb(state_data['channel_id'],
                                                     last_state=last_state,
                                                     condition_buttons_title=('✅ Включить', '❌ Отключить')))

    elif last_state == 'winner_count':
        await state.set_state()
        await message.answer(
            'Хотите добавить каналы-спонсоры?',
            reply_markup=contest_kb(state_data['channel_id'],
                                    last_state=last_state,
                                    condition_buttons_title=('✅ Да', '❌ Нет')))

    elif last_state == 'sponsor_channels':
        if not message.text.lower() == 'закончить':
            return await message.reply(f'Канал добавлен!\nЧтобы закончить напишите {hcode("Закончить")}.')
        await state.set_state()
        await message.answer(
            '📅 Когда опубликуем пост?',
            reply_markup=contest_kb(state_data['channel_id'], last_state=last_state,
                                    condition_buttons_title=('📆 В определённую дату', '🔜 Сразу')))

    elif last_state == 'start_at':
        await state.set_state()
        await message.answer(
            '⛔ Конкурс будет закончен в определённую дату или при достижении нужного количества участников?',
            reply_markup=contest_kb(state_data['channel_id'], last_state=last_state,
                                    condition_buttons_title=('👤 Учаcтники', '📆 Дата')))

    elif last_state in ['end_count', 'end_at']:
        await send_post(bot, message.from_user.id, state_data, post_button_kb(state_data['btn_title'], 0))  # 0 костыль

        if state_data['sponsor_channels']:
            sponsors_list = [await channel_db.get(tg_id=channel) for channel in state_data['sponsor_channels']]
            sponsors_list = [
                f"{chat_link(username=channel.username, tg_id=channel.tg_id, title=channel.title)}" for channel in sponsors_list]
            sponsors_list = ', '.join(sponsors_list)

        await message.answer(f"{hbold('👥 Кол-во победителей:')} {state_data['winner_count']}"
                             f"\n{hbold('▶ Публикация:')} {state_data['start_at'].strftime('в %H:%M %d.%m.%Y') if state_data['start_at'] else 'Сейчас'}"
                             f"\n{hbold('⏸ Окончание:')} {state_data['end_at'].strftime('в %H:%M %d.%m.%Y') if state_data['end_at'] else 'после %s участников' % (state_data['end_count'])}"
                             f"\n{hbold('🌐 Предпросмотр ссылок:')} {'✅' if state_data['is_attachment_preview'] else '❌'}"
                             f"\n{hbold('🌐 Каналы-спонсоры:')} {sponsors_list if state_data['sponsor_channels'] else '❌'}"
                             f"\n\n❗ Проверьте данные!",
                             reply_markup=contest_kb(state_data['channel_id'], last_state=last_state,
                                                     condition_buttons_title=['✔ Готово!']))

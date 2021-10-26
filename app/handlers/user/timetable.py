from datetime import timedelta
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from app.keyboards.timetable import TimetableKeyboard
from app.models.user import User
from app.utils.db_api.users import Users
from app.utils.db_api.weekdays import WeekDays
from app.utils.db_api.timetable import Timetable


def get_timetable(user: User, weekday: int) -> dict:
    '''Возвращает словарь для отправки сообщения с текстом расписания и parse_mode'''
    # get day_name
    day_name = WeekDays.get_day_name(weekday)

    # TODO: проблема с коммитом сессии, где получаем юзера
    # get timetable
    group = user.group
    class_ = user.class_
    timetable = Timetable.get(class_, group, weekday)
        
    # construct a message with the timetable
    lessons = []
    for les_num, subj_name, room, time_st, time_end in timetable:
        lessons.append(f'{les_num}. <b>{subj_name}</b>, {room}, <i>{time_st}-{time_end}</i>')
    
    text = f'<u>{day_name}</u>\n\n' + '\n\n'.join(lessons)
    concrete_day_kb = TimetableKeyboard.get_concrete_day_keyboard()

    return {
        'text': text,
        'parse_mode': types.ParseMode.HTML,
        'reply_markup': concrete_day_kb
        }


async def get_actual_days_timetable(message: types.Message):
    from_id = message.from_user.id
    user = Users.get(from_id)

    if user:
        text = message.text.lower()
        one_day = timedelta(days=1)

        if text == 'другой день':
            await message.answer('Хорошо! Выбери день',
             reply_markup=TimetableKeyboard.get_concrete_day_keyboard())
        else:
            if text == 'на сегодня':
                weekday = message.date.weekday() + 1
            elif text == 'на завтра':
                weekday = (message.date + one_day).weekday() + 1
            elif text == 'на вчера':
                weekday = (message.date - one_day).weekday() + 1

            if weekday == 6:
                weekday = 5
            elif weekday == 7:
                weekday = 1

            kwargs = get_timetable(user, weekday)
            await message.answer(**kwargs)
    else:
        await message.answer('Укажи в каком ты классе! Нажми на /start')


async def send_concrete_day_timetable(call: types.CallbackQuery, callback_data: dict):
    day_id = int(callback_data['day_id'])
    
    from_id = call.from_user.id
    user = Users.get(from_id)

    if user:
        kwargs = get_timetable(user, day_id)
        await call.message.answer(**kwargs)
    else:
        await call.message.answer('Укажи в каком ты классе! Нажми на /start')
    
    await call.answer()


def register_handlers_timetable(dp: Dispatcher):
    dp.register_message_handler(get_actual_days_timetable, Text(['На сегодня', 'На завтра', 'На вчера', 'Другой день'], ignore_case=True))
    dp.register_callback_query_handler(send_concrete_day_timetable, TimetableKeyboard.cb.filter())
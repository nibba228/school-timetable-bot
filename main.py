from datetime import timedelta
from typing import Union

from aiogram import executor, types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, Session
from keyboards import StartKeyboard, TimetableKeyboard
from models import User, Week
from timetable import Timetable


start_keyboard = StartKeyboard()
timetable_kb = TimetableKeyboard()


def get_timetable(user: User, weekday: int) -> dict:
    '''Возвращает словарь для отправки сообщения с текстом расписания и parse_mode'''
    # get day_name
    session = Session()
    day_name = session.query(Week).get(weekday).day_name
    session.commit()

    # get timetable
    group = user.group
    class_ = user.class_
    timetable = Timetable(class_, group, weekday)
    timetable = timetable.get()
        
    # construct a message with the timetable
    lessons = []
    for les_num, subj_name, room, time_st, time_end in timetable:
        lessons.append(f'{les_num}. <b>{subj_name}</b>, {room}, <i>{time_st}-{time_end}</i>')
        
    text = f'<u>{day_name}</u>\n\n' + '\n\n'.join(lessons)
    concrete_day_kb = timetable_kb.get_concrete_day_keyboard()

    return {
        'text': text,
        'parse_mode': types.ParseMode.HTML,
        'reply_markup': concrete_day_kb
        }



@dp.message_handler(CommandStart())
async def start(message: types.Message):
    text = 'Хай! Тут ты можешь посмотреть расписание школы 1568.' \
            '\nЧтобы понять по какому расписанию ты существуешь,'\
            '\nмне нужно узнать в каком ты классе и группе учишься.\n'\
            '\nВыбери класс'

    keyboard = start_keyboard.get_keyboard_class_num()
    
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(start_keyboard.cb.filter())
async def manage_class_data(call: types.CallbackQuery, callback_data: dict):
    num = callback_data['num']
    letter = callback_data['letter']
    group = callback_data['group']
    
    session = Session()
    is_registered = session.query(User)\
                    .filter(User.from_id == call.from_user.id)\
                    .count()
    session.commit()

    if not is_registered:
        if letter == '0':
            letter_keyboard = start_keyboard.get_keyboard_class_letter(num)
            await call.message.edit_text('Хорошо! А какая буква?', reply_markup=letter_keyboard)
        elif group == '0':
            group_keyboard = start_keyboard.get_keyboard_group(num, letter)
            await call.message.edit_text('Ну просто супер!\nОсталась только группа',
            reply_markup=group_keyboard)
        elif group in '12':
            session = Session()
            user = User(
                from_id=call.from_user.id,
                class_=str(num) + letter,
                group=int(group)
            )

            session.add(user)
            session.commit()

            timetable_reply_kb = timetable_kb.get_keyboard()
            await call.message.answer('Замечательно! Теперь ты можешь запрашивать расписание!',
                                            reply_markup=timetable_reply_kb)
    else:
        timetable_reply_kb = timetable_kb.get_keyboard()
        await call.message.answer('Ты уже зарегистрирован!', reply_markup=timetable_reply_kb)
    
    await call.answer()


@dp.message_handler(Text(['На сегодня', 'На завтра', 'На вчера', 'Другой день'], ignore_case=True))
async def get_today_timetable(message: types.Message):
    session = Session()
    from_id = message.from_user.id
    user = session.query(User).get(from_id)
    session.commit()

    if user:
        text = message.text.lower()
        one_day = timedelta(days=1)

        if text == 'другой день':
            await message.answer('Хорошо! Выбери день',
             reply_markup=timetable_kb.get_concrete_day_keyboard())
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
    

@dp.callback_query_handler(timetable_kb.cb.filter())
async def send_concrete_day_timetable(call: types.CallbackQuery, callback_data: dict):
    day_id = int(callback_data['day_id'])
    
    session = Session()
    from_id = call.from_user.id
    user = session.query(User).get(from_id)
    session.commit()

    if user:
        kwargs = get_timetable(user, day_id)
        await call.message.answer(**kwargs)
    else:
        await call.message.answer('Укажи в каком ты классе! Нажми на /start')
    
    await call.answer()
    

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer('Извини, я тебя не понял')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
import os
from aiogram import executor, types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, Session
from keyboards import StartKeyboard, TimetableKeyboard
from models import User

start_keyboard = StartKeyboard()

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
            letter_keyboard = start_keyboard.get_ketboard_class_letter(num)
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

            timetable_kb = TimetableKeyboard.get_keyboard()
            await call.message.answer('Замечательно! теперь ты можешь запрашивать расписание!',
                                            reply_markup=timetable_kb)
    else:
        await call.message.answer('Ты уже зарегистрирован!')
    
    await call.answer()


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
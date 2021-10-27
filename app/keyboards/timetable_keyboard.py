from aiogram import types
from aiogram.utils.callback_data import CallbackData


class TimetableKeyboard:
    
    cb = CallbackData('day', 'day_id')

    @staticmethod
    def get_keyboard():
        '''Клавиатура с актуальными днями для получения расписания'''

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        yesterday = types.KeyboardButton('На вчера')
        tomorrow = types.KeyboardButton('На завтра')
        today = types.KeyboardButton('На сегодня')
        other = types.KeyboardButton('Другой день')

        keyboard.add(yesterday, tomorrow, today, other)
        return keyboard
    
    @staticmethod    
    def get_concrete_day_keyboard():
        '''Клавиатура для получения расписания на конкретный день'''

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        days = 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'
        buttons = []

        for day_id in range(len(days)):
            buttons.append(types.InlineKeyboardButton(days[day_id],
             callback_data=TimetableKeyboard.cb.new(day_id=day_id + 1)))
        
        keyboard.add(*buttons)

        return keyboard

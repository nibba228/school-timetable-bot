from aiogram import types
from aiogram.utils.callback_data import CallbackData


class StartKeyboard:
    def __init__(self):
        self.cb = CallbackData('class', 'num', 'letter', 'group')

    def get_keyboard_class_num(self):
        '''Клавиатура для получения номера класса'''

        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=str(i),
                     callback_data=self.cb.new(num=i, letter='0', group=0)) 
                    for i in range(5, 12)]

        keyboard.add(*buttons[:3])
        keyboard.add(*buttons[3:5])
        keyboard.add(*buttons[5:])

        return keyboard
    
    def get_keyboard_class_letter(self, num: int):
        '''Клавиатура для получения буквы класса'''

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        alphabet = 'абвгикл'

        buttons = [types.InlineKeyboardButton(text=str(num) + a,
                    callback_data=self.cb.new(num=num, letter=a, group=0))
                    for a in alphabet]
        keyboard.add(*buttons)

        return keyboard
    
    def get_keyboard_group(self, num: int, letter: str):
        '''Клавиатура для получения номера группы'''

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [types.InlineKeyboardButton(text=i,
                    callback_data=self.cb.new(num=num, letter=letter, group=i))
                    for i in (1, 2)]
        keyboard.add(*buttons)

        return keyboard


class TimetableKeyboard:
    @staticmethod
    def get_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        yesterday = types.KeyboardButton('На вчера')
        tomorrow = types.KeyboardButton('На завтра')
        today = types.KeyboardButton('На сегодня')

        keyboard.add(yesterday, tomorrow, today)
        return keyboard
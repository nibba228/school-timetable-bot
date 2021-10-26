from aiogram import types
from aiogram.utils.callback_data import CallbackData


class StartKeyboard:
    
    cb = CallbackData('class', 'num', 'letter', 'group')

    @staticmethod
    def get_keyboard_class_num():
        '''Клавиатура для получения номера класса'''

        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=str(i),
                     callback_data=StartKeyboard.cb.new(num=i, letter='0', group=0)) 
                    for i in range(5, 12)]

        keyboard.add(*buttons[:3])
        keyboard.add(*buttons[3:5])
        keyboard.add(*buttons[5:])

        return keyboard
    
    @staticmethod
    def get_keyboard_class_letter(num: int):
        '''Клавиатура для получения буквы класса'''

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        alphabet = 'абвгикл'

        buttons = [types.InlineKeyboardButton(text=str(num) + a,
                    callback_data=StartKeyboard.cb.new(num=num, letter=a, group=0))
                    for a in alphabet]
        keyboard.add(*buttons)

        return keyboard
    
    @staticmethod
    def get_keyboard_group(num: int, letter: str):
        '''Клавиатура для получения номера группы'''

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [types.InlineKeyboardButton(text=i,
                    callback_data=StartKeyboard.cb.new(num=num, letter=letter, group=i))
                    for i in (1, 2)]
        keyboard.add(*buttons)

        return keyboard

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command

from app.states.user.classes import ChoosingClass
from app.keyboards.start_keyboard import StartKeyboard
from app.utils.db_api.users import Users
from loader import logger


@logger.catch
async def start(message: types.Message, state: FSMContext):
    text = 'Привет! Тут ты можешь посмотреть расписание школы 1568.' \
            '\nЧтобы понять по какому расписанию ты существуешь,'\
            '\nмне нужно узнать в каком ты классе и группе учишься.\n'\
            '\nВыбери класс'

    keyboard = StartKeyboard.get_keyboard_class_num()
    
    if state:
        await state.finish()
    await ChoosingClass.choosing_class_num.set()
    logger.info('Пользователь {} поменял состояние на {}', message.from_user.id, str(ChoosingClass.choosing_class_num))
    await logger.complete()
    await message.answer(text, reply_markup=keyboard)


@logger.catch
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    logger.info('Пользователь {} отменил действие', message.from_user.id)
    await logger.complete()
    await message.answer('Действие отменено')


@logger.catch
async def reset(message: types.Message, state: FSMContext):
    user = Users.get(message.from_user.id)
    if user:
        Users.delete(user)
        await state.finish()
        await message.answer('Класс и группа сброшены')
    else:
        await message.answer('Ты не зарегистрирован(а)! Чтобы зарегистрироваться, нажми на /start')


@logger.catch
async def misunderstood_msg(message: types.Message):
    await message.answer('Извини, я тебя не понял')


@logger.catch
def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), state='*')
    dp.register_message_handler(cancel, Command('cancel'), state='*')
    dp.register_message_handler(reset, Command('reset'), state='*')
    dp.register_message_handler(misunderstood_msg)

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.keyboards.start_keyboard import StartKeyboard
from app.keyboards.timetable_keyboard import TimetableKeyboard
from app.states.user.classes import ChoosingClass
from app.utils.db_api.users import Users
from loader import logger


@logger.catch
async def choose_class_num(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    class_num = int(callback_data['num'])
    await state.update_data(chosen_num=class_num)

    from_id = call.from_user.id
    user = Users.get(from_id)

    if not user:
        letter_keyboard = StartKeyboard.get_keyboard_class_letter(class_num)

        await ChoosingClass.next()
        logger.info('Пользователь {} поменял состояние на {}', call.from_user.id, await state.get_state())
        await logger.complete()
        await call.message.edit_text('Хорошо! А какая буква?', reply_markup=letter_keyboard)
    else:
        await state.finish()
        timetable_kb = TimetableKeyboard.get_keyboard()
        await call.message.answer('Ты уже зарегистрирован!', reply_markup=timetable_kb)

    await call.answer()


@logger.catch
async def choose_letter(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    letter = callback_data['letter']
    await state.update_data(chosen_letter=letter)
    class_info = await state.get_data()

    keyboard = StartKeyboard.get_keyboard_group(class_info['chosen_num'], letter)

    await ChoosingClass.next()
    logger.info('Пользователь {} поменял состояние на {}', call.from_user.id, await state.get_state())
    await logger.complete()
    await call.message.edit_text('Ну просто супер!\nОсталась только группа', reply_markup=keyboard)

    await call.answer()


@logger.catch
async def choose_group(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    group = int(callback_data['group'])
    class_data = await state.get_data()

    from_id = call.from_user.id
    class_ = str(class_data['chosen_num']) + class_data['chosen_letter']
    Users.insert(from_id, class_, group)
    
    await state.finish()

    keyboard = TimetableKeyboard.get_keyboard()
    await call.message.answer('Замечательно! Теперь ты можешь запрашивать расписание!',
                                            reply_markup=keyboard)
    await call.answer()


@logger.catch
async def already_registered(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = Users.get(call.from_user.id)

    if user:
        timetable_kb = TimetableKeyboard.get_keyboard()
        await call.message.answer('Ты уже зарегистрирован!', reply_markup=timetable_kb)
    else:
        await call.message.answer('Зарегистрируйся, нажми на /start')

    await call.answer()


@logger.catch
def register_handlers_choosing_class(dp: Dispatcher):
    dp.register_callback_query_handler(choose_class_num, StartKeyboard.cb.filter(),
                                       state=ChoosingClass.choosing_class_num)
    dp.register_callback_query_handler(choose_letter, StartKeyboard.cb.filter(), 
                                       state=ChoosingClass.choosing_class_letter)
    dp.register_callback_query_handler(choose_group, StartKeyboard.cb.filter(),
                                       state=ChoosingClass.choosing_class_group)
    dp.register_callback_query_handler(already_registered, StartKeyboard.cb.filter(), state='*')
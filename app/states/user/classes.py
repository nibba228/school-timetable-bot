from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ChoosingClass(StatesGroup):
    choosing_class_num = State()
    choosing_class_letter = State()
    choosing_class_group = State()

from aiogram.dispatcher.filters.state import State, StatesGroup

class Registration(StatesGroup):
    group_name = State()

class Unreg(StatesGroup):
    user_answer = State()
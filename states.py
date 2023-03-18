from aiogram.dispatcher.filters.state import State, StatesGroup


class Password(StatesGroup):
    waiting_for_registration = State()
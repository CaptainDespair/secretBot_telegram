from aiogram.dispatcher.filters.state import State, StatesGroup

class Password(StatesGroup):
    waiting_for_registration = State()
    waiting_for_authorization_rd = State()
    waiting_for_authorization_wrt = State()
    waiting_for_write_data = State()
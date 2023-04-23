from aiogram.dispatcher.filters.state import State, StatesGroup

class Password(StatesGroup):
    waiting_for_reg_user = State()
    waiting_for_wrt_data = State()
    waiting_for_auth_rd = State()
    waiting_for_auth_wrt = State()
    waiting_for_auth_dlt_data = State()
    waiting_for_auth_dlt_user = State()
    
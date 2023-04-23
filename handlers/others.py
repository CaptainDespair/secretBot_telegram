from aiogram import types, Dispatcher

from create_bot import dp, bot

#Any messages
async def send_hello(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет! Напиши /start или /help')

def register_client_handlers(dp : Dispatcher):
    dp.register_message_handler(send_hello)  
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

async def on_startup(_):    
    print('Bot is working') 

#CLIENT==========================================================================================
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 
                           f'Приветствую, твой id={message.from_user.id}. Выбери действие')

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 
                           f'Приветствую, {message.from_user.id}. Я умею надежно хранить твои пароли и информацию!')

@dp.message_handler(commands=['Регистрация'])
async def registation(message: types.Message):
    await bot.send_message(message.from_user.id, f'{message.from_user.id}, придумайте пароль.')

@dp.message_handler()
async def validation(message: types.Message):
    if ' ' in message.text:
        await message.reply(f'{message.from_user.id}, пароль не должен содержать пробелы!')
        await message.delete()
    else: 
        hiden_password = len(message.text)*'*'
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, пароль {hiden_password} успешно сохранен.')
        await message.delete()

@dp.message_handler(commands=['Мои секреты'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 
                           f'{message.from_user.id}, введите пароль.')
    
#=================================================================================================
    
@dp.message_handler()
async def send_id(message: types.Message):
    await bot.send_message(message.from_user.id, f'Напиши /start или /help')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
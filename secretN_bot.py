from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import json
import config, states


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

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
    await bot.send_message(message.from_user.id, 
                           'Введи одну из команд:\n/Регистрация : регистрирует пользователей в нашей системе\n/Мои секреты : ваша БД')


@dp.message_handler(commands=['Регистрация'])
async def registation(message: types.Message,):
    with open('passwords.json', 'r') as pw:
        if str(message.from_user.id) + '_password":' in pw.read():
            await bot.send_message(message.from_user.id, 
                                f'{message.from_user.id}, вы уже регистрировались здесь!')
        else:
            await bot.send_message(message.from_user.id, 
                                f'{message.from_user.id}, придумайте пароль.') 
            await states.Password.waiting_for_registration.set()


@dp.message_handler(state=states.Password.waiting_for_registration)              
async def validation(message: types.Message, state: FSMContext):
    password = message.text
    hiden_password = len(message.text)*'*'
    await state.update_data(password=password)

    if ' ' in password:
        await bot.send_message(message.from_user.id, 
                               f'{message.from_user.id}, пароль не должен содержать пробелы!')
        await message.delete()
    else:
        password_conc = str(message.from_user.id) + '_password'
        password_to_db = {password_conc : message.text}

        with open('passwords.json') as pw:
            data = json.load(pw)
            data['passwords'].append(password_to_db)
            with open('passwords.json', 'w') as outpw:
                json.dump(data, outpw)

        await bot.send_message(message.from_user.id, 
                                f'{message.from_user.id}, пароль {hiden_password} успешно сохранен.')
        await message.delete()                
    
    await state.finish()


@dp.message_handler(commands=['Мои секреты'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 
                           f'{message.from_user.id}, введите пароль.')
    
#================================================================================================= 
@dp.message_handler()
async def send_id(message: types.Message):
    await bot.send_message(message.from_user.id, f'Напиши /start или /help')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
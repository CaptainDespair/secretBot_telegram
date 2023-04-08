from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import states

import json

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def on_startup(_):    
    print('Bot is working') 

#CLIENT-API
#---------------------------------------------
#/start, /help
@dp.message_handler(commands=['start','help'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, 
                           f'Приветствую, твой id={message.from_user.id}.\
                            \nЯ умею надежно хранить твои пароли и информацию!')
    await bot.send_message(message.from_user.id, 
                           'Введи одну из команд:\
                            \n/Регистрация : регистрирует пользователей в нашей системе\
                            \n/Мои_данные : ваша БД\
                            \n/Добавить_данные : добавить данные в вашу БД')

#/Регистрация
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

#/Мои_данные
@dp.message_handler(commands=['Мои_данные'])
async def data_read(message: types.Message):
    with open('passwords.json') as pw:
        if str(message.from_user.id) + '_password":' not in pw.read():
            await bot.send_message(message.from_user.id, f'{message.from_user.id}, вы не зарегистрированы.\
                                   Обратитесь к команде "/Регистрация", чтобы внести данные в базу данных ')
        else:     
            await bot.send_message(message.from_user.id, 
                                f'{message.from_user.id}, введите пароль.')
            await states.Password.waiting_for_authorization_rd.set()

#/Добавить_данные
@dp.message_handler(commands=['Добавить_данные'])
async def data_write(message: types.Message):
    with open('passwords.json') as pw:
        if str(message.from_user.id) + '_password":' not in pw.read():
            await bot.send_message(message.from_user.id, f'{message.from_user.id}, вы не зарегистрированы.\
                                   Обратитесь к команде "/Регистрация", чтобы внести данные в базу данных ')
        else:     
            await bot.send_message(message.from_user.id, 
                                f'{message.from_user.id}, введите пароль.')
            await states.Password.waiting_for_authorization_wrt.set()

#Создание пароля
@dp.message_handler(state=states.Password.waiting_for_registration)              
async def validationDuringReg(message: types.Message, state: FSMContext):
    password = message.text
    hiden_password = len(message.text)*'*'
    await state.update_data(password=password)
    if ' ' in password:
        await bot.send_message(message.from_user.id, 
                               f'{message.from_user.id}, пароль не должен содержать пробелы!')
        await message.delete()
    else:
        user_password = str(message.from_user.id) + '_password'
        password_to_db = {user_password : password}

        with open('passwords.json') as pw:
            data = json.load(pw)
            data['passwords'].append(password_to_db)
            with open('passwords.json', 'w') as outpw:
                json.dump(data, outpw)

        await bot.send_message(message.from_user.id, 
                                f'{message.from_user.id}, пароль {hiden_password} успешно сохранен.')
        await message.delete()                
    
    await state.finish()

#Авторизация чтение даных
@dp.message_handler(state=states.Password.waiting_for_authorization_rd)
async def validationDuringAuth(message: types.Message, state: FSMContext):
    password = message.text
    user_password = str(message.from_user.id) + '_password'
    password_in_db = f'"{user_password}": "{password}"'
    user_data = str(message.from_user.id) + '_data'

    with open('passwords.json') as pw:
        if password_in_db in pw.read():
            await bot.send_message(message.from_user.id, 'Успешно, чтение')
            with open('data.json') as pw:
                data = json.load(pw)
                print(user_data, data["data"])
                print(type(user_data), type(data["data"]))
                
                for d in data["data"]:
                    if user_data in d:
                        print(d[user_data])
                        await bot.send_message(message.from_user.id, f'{d[user_data]}')
        else:
            await bot.send_message(message.from_user.id, 'НЕВЕРНО!')  

    await message.delete()                  

#Авторизация запись данных
@dp.message_handler(state=states.Password.waiting_for_authorization_wrt)
async def validationDuringAuth(message: types.Message, state: FSMContext):
    password = message.text
    user_password = str(message.from_user.id) + '_password'
    password_in_db = f'"{user_password}": "{password}"'
    
    with open('passwords.json') as pw:
        if password_in_db in pw.read():
            await bot.send_message(message.from_user.id, 'Успешно. Внесите данные.')
            await states.Password.waiting_for_write_data.set()
        else:
            await bot.send_message(message.from_user.id, 'НЕВЕРНО!')
    await message.delete()
    
#Запись данных    
@dp.message_handler(state=states.Password.waiting_for_write_data)   
async def write_data(message: types.Message, state: FSMContext):         
    user = str(message.from_user.id) + '_data'
    user_data = str(message.text)
    data_to_db = {user : user_data}

    with open('data.json') as pw:
        data = json.load(pw)
        data['data'].append(data_to_db)
        with open('data.json', 'w') as outpw:
            json.dump(data, outpw)
    await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, данные успешно занесены.')                  
    await state.finish()
    await message.delete()

# #--------------------------------------

#Any messages
@dp.message_handler()
async def send_id(message: types.Message):
    await bot.send_message(message.from_user.id, f'Напиши /start или /help')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
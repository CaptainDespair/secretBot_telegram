from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from sqlalchemy.orm import sessionmaker

import states

from config import TOKEN
from create_db import engine
from models import User, Data


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

Session = sessionmaker(bind=engine)
session = Session()

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
async def registation(message: types.Message):
    name_id  = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы уже регистрировались здесь!')
    else:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, придумайте пароль.') 
        await states.Password.waiting_for_registration.set()
    
#/Мои_данные
@dp.message_handler(commands=['Мои_данные'])
async def data_read(message: types.Message):
    name_id = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.')
        await states.Password.waiting_for_authorization_rd.set()
    else:     
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"/Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')

#/Добавить_данные
@dp.message_handler(commands=['Добавить_данные'])
async def data_write(message: types.Message):
    name_id = str(message.from_user.id)
    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.')
        await states.Password.waiting_for_authorization_wrt.set() 
    else:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"/Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')
            
#Создание пароля
@dp.message_handler(state=states.Password.waiting_for_registration)              
async def create_correct_password(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text
    hiden_password = len(message.text)*'*'
    #await state.update_data(password=password)
    
    if ' ' in password:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, пароль не должен содержать пробелы!')
        await message.delete()
    else:
        user = User(name_id=name_id, password=password)
        session.add(user)
        session.commit()
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, пароль {hiden_password} успешно сохранен.\
                            \nПользователь {message.from_user.id} зарегестрирован.')
        await message.delete()                
        await state.finish()

#Авторизация на чтение данных
@dp.message_handler(state=states.Password.waiting_for_authorization_rd)
async def read_user_data(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text

    password_is_valid = session\
                     .query(User)\
                     .filter_by(name_id=name_id, password=password)\
                     .first()
    session.close()

    if password_is_valid:
        await bot.send_message(message.from_user.id, 
                               'ВАШИ ДАННЫЕ:\n-------------------------')
        data = session\
                .query(Data)\
                .filter_by(user_id=password_is_valid.id)\
                .all()
        for frame in data:
            await bot.send_message(message.from_user.id,
                                   f'{frame}\n')  
        await bot.send_message(message.from_user.id,
                               '<b><i>В качестве безопасности очистите историю.\
                               Ваши данные будут сохранены.</i></b>', 
                               parse_mode='HTML')                                
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Неверный пароль!')  

    await message.delete()                  

#Авторизация на запись данных
@dp.message_handler(state=states.Password.waiting_for_authorization_wrt)
async def auth_valid(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text

    password_is_valid = session\
                     .query(User)\
                     .filter_by(name_id=name_id, password=password)\
                     .first()
    session.close()

    if password_is_valid:
        await bot.send_message(message.from_user.id, 
                               'Успешно. Внесите ваши данные')
        await states.Password.waiting_for_write_data.set()
    else:
        await bot.send_message(message.from_user.id, 
                               'Неверный пароль!')
    await message.delete()
    
#Запись данных    
@dp.message_handler(state=states.Password.waiting_for_write_data)   
async def write(message: types.Message, state: FSMContext):         
    name_id = str(message.from_user.id)
    data = str(message.text)

    get_user_id = session\
                  .query(User)\
                  .filter_by(name_id=name_id)\
                  .first()
    session.close()

    data = Data(text=data, user_id=get_user_id.id)
    session.add(data)
    session.commit()
    await bot.send_message(message.from_user.id, 
                        f'{message.from_user.id}, данные успешно занесены.')  
                    
    await state.finish()
    await message.delete()

#Any messages
@dp.message_handler()
async def send_hello(message: types.Message):
    await bot.send_message(message.from_user.id, f'Напиши /start или /help')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

#--------------------------------------
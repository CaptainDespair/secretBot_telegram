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
async def command_start_help(message: types.Message):
    await bot.send_message(message.from_user.id, 
                           f'Приветствую, твой id={message.from_user.id}.\
                            \nЯ умею надежно хранить твои пароли и информацию!')
    await bot.send_message(message.from_user.id, 
                           'Введи одну из команд:\
                            \n/Регистрация : регистрирует пользователей в нашей системе\
                            \n/Мои_данные : ваша БД\
                            \n/Добавить_данные : добавить данные в вашу БД\
                            \n/Удалить_данные : удалить данные в БД\
                            \n/Удалить_учетную_запись: удалить учетную запись и вашу БД')


#/Регистрация
@dp.message_handler(commands=['Регистрация'])
async def command_registration(message: types.Message):
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
        await states.Password.waiting_for_reg_user.set()
            

#Создание пароля
@dp.message_handler(state=states.Password.waiting_for_reg_user)              
async def create_corr_password(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text
    hiden_password = len(message.text)*'*'
    
    try:
        get_max_id = session\
                        .query(User)\
                        .order_by(User.id.desc())\
                        .first()
        session.close()
        max_id = get_max_id.id + 1
    except: 
        max_id = 0

    if ' ' in password:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, пароль не должен содержать пробелы!')
        await message.delete()
    else:
        user = User(id = max_id, name_id=name_id, password=password)
        session.add(user)
        session.commit()
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, пароль {hiden_password} успешно сохранен.\
                            \nПользователь {message.from_user.id} зарегестрирован.')
        await message.delete()                
        await state.finish()


#/Мои_данные
@dp.message_handler(commands=['Мои_данные'])
async def command_read_data(message: types.Message):
    name_id = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.')
        await states.Password.waiting_for_auth_rd.set()
    else:     
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"/Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')


#Авторизация и чтение данных
@dp.message_handler(state=states.Password.waiting_for_auth_rd)
async def auth_for_read(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text

    password_is_valid = session\
                     .query(User)\
                     .filter_by(name_id=name_id, password=password)\
                     .first()
    session.close()

    if password_is_valid:
        get_user_id = password_is_valid.id
        await bot.send_message(message.from_user.id, 
                               'ВАШИ ДАННЫЕ:\n-------------------------')
        data = session\
                .query(Data)\
                .filter_by(user_id=get_user_id)\
                .all()
        for frame in data:
            await bot.send_message(message.from_user.id,
                                   f'{frame.text} \n')  
        await bot.send_message(message.from_user.id,
                               '<b><i>В качестве безопасности очистите историю.\
                               Ваши данные будут сохранены.</i></b>', 
                               parse_mode='HTML')                                
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Неверный пароль!')  

    await message.delete()                  


#/Добавить_данные
@dp.message_handler(commands=['Добавить_данные'])
async def command_write_data(message: types.Message):
    name_id = str(message.from_user.id)
    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.')
        await states.Password.waiting_for_auth_wrt.set() 
    else:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"/Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')


#Авторизация на запись данных
@dp.message_handler(state=states.Password.waiting_for_auth_wrt)
async def auth_for_write(message: types.Message, state: FSMContext):
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
        await states.Password.waiting_for_wrt_data.set()
    else:
        await bot.send_message(message.from_user.id, 
                               'Неверный пароль!')
    await message.delete()
    

#Запись данных    
@dp.message_handler(state=states.Password.waiting_for_wrt_data)   
async def write_data(message: types.Message, state: FSMContext):         
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


#/Удалить_данные
@dp.message_handler(commands=['Удалить_данные'])
async def command_delete_data(message: types.Message):
    name_id = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.')
        await states.Password.waiting_for_auth_dlt_data.set()
    else:     
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"/Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')
        
        
#Авторизация на удаление данных
@dp.message_handler(state=states.Password.waiting_for_auth_dlt_data)
async def auth_for_delete(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text

    password_is_valid = session\
                     .query(User)\
                     .filter_by(name_id=name_id, password=password)\
                     .first()
    session.close()

    try:
        get_user_id = password_is_valid.id
    except:
        await bot.send_message(message.from_user.id, 
                               'Неверный пароль!')

    if password_is_valid:
        await bot.send_message(message.from_user.id, 
                               'Успешно. Происходит удаление...')
        
        session.query(Data).filter_by(user_id=get_user_id).delete()
        session.commit()

        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, данные успешно удалены.')     
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 
                               'Неверный пароль!')
    await message.delete()


#/Удалить_учетную_запись
@dp.message_handler(commands=['Удалить_учетную_запись'])
async def command_delete_user(message: types.Message):
    name_id = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.')
        await states.Password.waiting_for_auth_dlt_user.set()
    else:     
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"/Регистрация"</i></b>',
                               parse_mode='HTML')
        
        
#Авторизация на удаление пользователя
@dp.message_handler(state=states.Password.waiting_for_auth_dlt_user)
async def auth_for_delete_user(message: types.Message, state: FSMContext):
    name_id = str(message.from_user.id)
    password = message.text

    password_is_valid = session\
                     .query(User)\
                     .filter_by(name_id=name_id, password=password)\
                     .first()
    session.close()

    if password_is_valid:
        get_user_id = password_is_valid.id
        session.query(User).filter_by(id=get_user_id).delete()
        session.commit()

        await bot.send_message(message.from_user.id, 
                            f'Пользватель {message.from_user.id} и даные удалены.')     
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 
                               'Неверный пароль!')
    await message.delete()


#Any messages
@dp.message_handler()
async def send_hello(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет! Напиши /start или /help')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

#--------------------------------------
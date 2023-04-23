from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import dp, bot, session
from database.models import User, Data
from keyboards import client_keyboard

import states


async def command_start_help(message: types.Message):
    ''' /start, /help'''
    
    await bot.send_message(message.from_user.id, 
                           f'Приветствую, твой id=<b>{message.from_user.id}</b>.\
                            \nЯ умею надежно хранить твои пароли и информацию!',
                            parse_mode='HTML',
                            reply_markup=client_keyboard)
    await bot.send_message(message.from_user.id, 
                           'Введи одну из команд:\
                            \n\n<b><i>Регистрация</i></b> : регистрирует пользователей в нашей системе\
                            \n<b><i>Мои данные</i></b> : ваша БД\
                            \n<b><i>Добавить данные</i></b> : добавить данные в вашу БД\
                            \n<b><i>Удалить данные</i></b> : удалить данные в БД\
                            \n<b><i>Удалить учетную запись</i></b> : удалить учетную запись и вашу БД\
                            \n\n<i>Если вдруг вы забыли пароль или у вас возникли ошибки, обратитесь к администратору</i>',
                            parse_mode='HTML')


async def command_registration(message: types.Message):
    '''/Регистрация'''

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
                            f'{message.from_user.id}, придумайте пароль. <b>Обязательно запомните его!</b>',
                            parse_mode='HTML') 
        await states.Password.waiting_for_reg_user.set()
            

async def create_corr_password(message: types.Message, state: FSMContext):
    '''Создание корректного пароля'''

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
                            \nПользователь <b>{message.from_user.id}</b> зарегестрирован.',
                            parse_mode='HTML')
        await message.delete()                
        await state.finish()


async def command_read_data(message: types.Message):
    '''/Мои данные'''

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
                              \nОбратитесь к команде <b><i>"Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')


async def auth_for_read(message: types.Message, state: FSMContext):
    '''Авторизация и чтение данных'''

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
                               '<b>ВАШИ ДАННЫЕ:\n-------------------------</b>',
                               parse_mode='HTML')
        data = session\
                .query(Data)\
                .filter_by(user_id=get_user_id)\
                .all()
        for frame in data:
            await bot.send_message(message.from_user.id,
                                   f'{frame.text} \n')  
        await bot.send_message(message.from_user.id,
                               '<b><i>В качестве безопасности очистите историю.\
                               \nВаши данные будут сохранены.</i></b>', 
                               parse_mode='HTML')                                
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Неверный пароль!') 
        await state.finish() 

    await message.delete()                  


async def command_write_data(message: types.Message):
    '''/Добавить данные'''

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
                              \nОбратитесь к команде <b><i>"Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')


async def auth_for_write(message: types.Message, state: FSMContext):
    '''Авторизация на запись данных'''

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
    
     
async def write_data(message: types.Message, state: FSMContext):   
    '''Запись данных'''      
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


async def command_delete_data(message: types.Message):
    '''/Удалить данные'''

    name_id = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.\
                              \n\n<i>Если вы оказались тут по ошибке, введите рандомный набор символов</i>',
                              parse_mode='HTML')
        await states.Password.waiting_for_auth_dlt_data.set()
    else:     
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"Регистрация"</i></b>,\
                              \nчтобы внести данные в базу данных.',
                              parse_mode='HTML')
        
        
async def auth_for_delete_data(message: types.Message, state: FSMContext):
    '''Авторизация на удаление данных'''

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
        pass

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
        await state.finish()

    await message.delete()


async def command_delete_user(message: types.Message):
    '''/Удалить учетную запись'''

    name_id = str(message.from_user.id)

    name_id_exist = session\
                    .query(User)\
                    .filter_by(name_id=name_id)\
                    .first()
    session.close()

    if name_id_exist:
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, введите пароль.\
                              \n\n<i>Если вы оказались тут по ошибке, введите рандомный набор символов</i>',
                              parse_mode='HTML')
        await states.Password.waiting_for_auth_dlt_user.set()
    else:     
        await bot.send_message(message.from_user.id, 
                            f'{message.from_user.id}, вы не зарегистрированы.\
                              \nОбратитесь к команде <b><i>"Регистрация"</i></b>',
                               parse_mode='HTML')
        
        
async def auth_for_delete_user(message: types.Message, state: FSMContext):
    '''Авторизация на удаление пользователя'''
    
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
                            f'Пользватель <b>{message.from_user.id}</b> и даные удалены.',
                            parse_mode='HTML')     
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 
                               'Неверный пароль!')
        await state.finish()

    await message.delete()

def register_client_handlers(dp : Dispatcher):
    dp.register_message_handler(command_start_help, 
                                commands=['start','help'])  
    dp.register_message_handler(command_registration,
                                text='Регистрация') 
    dp.register_message_handler(create_corr_password,
                                state=states.Password.waiting_for_reg_user) 
    dp.register_message_handler(command_read_data,
                                text='Мои данные') 
    dp.register_message_handler(auth_for_read,
                                state=states.Password.waiting_for_auth_rd) 
    dp.register_message_handler(command_write_data,
                                text='Добавить данные') 
    dp.register_message_handler(auth_for_write,
                                state=states.Password.waiting_for_auth_wrt)
    dp.register_message_handler(write_data,
                                state=states.Password.waiting_for_wrt_data)
    dp.register_message_handler(command_delete_data,
                                text='Удалить данные')
    dp.register_message_handler(auth_for_delete_data,
                                state=states.Password.waiting_for_auth_dlt_data)
    dp.register_message_handler(command_delete_user,
                                text='Удалить учетную запись')
    dp.register_message_handler(auth_for_delete_user,
                                state=states.Password.waiting_for_auth_dlt_user)
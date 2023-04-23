from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('Регистрация')
b2 = KeyboardButton('Мои данные')
b3 = KeyboardButton('Добавить данные')
b4 = KeyboardButton('Удалить данные')
b5 = KeyboardButton('Удалить учетную запись')

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

client_keyboard.row(b2,b1).row(b3,b4).add(b5)
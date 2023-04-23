# secretBot_telegram
<h3><i>TelegramBot name: @secretN_bot</i></h3>
<h4><i>в глобальном смысле проект закончен</i></h4>

Экспериментальный бот на Aiogram, регистрирует, сохраняет секретную информацию пользователей и удаляет по запросу. Реализация с помощью конечных автоматов.

Стек: 

- Python3.9

- Aiogram

- psycopg2

- Sqlalchemy

- PostgresSQL


Реализованы комманды: 

- Регистрация : регистрирует пользователей в нашей системе

- Мои данные : ваша БД

- Добавить данные : добавить данные в вашу БД

- Удалить данные : удалить данные из вашей БД

- Удалить учетную запись : удалить учетную запись вместе с записями (cascade)

<h2><b>Структура</b></h2> 

- database:
  - create_db.py вам нужно как минимум один раз запустить create_db.py, чтобы произвести миграции таблиц в бд. (postgresSQL)
  - connection_db.py - простое подключение к postgres
  - models.py - здесь модели (таблицы) User, Data

- handlers:
  - client.py логика API-телеграма для клиентов соответственно 

- keyboards:
  - client_buttons.py - логика кнопок
<h2><b>Скрытая структура</b></h2> 

<b>config.py:</b>

  TOKEN="<your_token>"

  DB_NAME = 'postgresql'

  PG_USER = 'postgres'

  PG_PASSWORD = "<your_password>"

  PG_HOST = '127.0.0.1'

  PG_PORT = '5432'

  PG_DATABASE_NAME = '<db_name>'

  PG_URL = f'{DB_NAME}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE_NAME}'
  
 <h2><b>Запуск приложения</b></h2> 

>pip install -r requirements

>python secretBot.py

<h3><i>TelegramBot name: @secretN_bot</i></h3>
<i>(*продакшн не планируется)</i>

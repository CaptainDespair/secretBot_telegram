import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import create_engine

from models import Base
from config import POSTGRES_PASSWORD

user = 'postgres'
password = POSTGRES_PASSWORD
host = '127.0.0.1'
port = '5432'
database = 'secret_db'

db_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(db_url)

def create_db():
    try:
        connection = psycopg2.connect(user=user,
                                      password=POSTGRES_PASSWORD,
                                      host=host,
                                      port=port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        cursor.execute(f'create database {database}')
        print('База данных создана успешно')
        cursor.close()

        connection.close()

        print("Соединение с PostgreSQL закрыто")

    except (Exception, Error) as error:
        print(error)


def create_tables():
    try:
        Base.metadata.create_all(engine)
        print('Таблицы созданы успешно')
    except (Exception, Error) as error:
        print('Возникли ошибки', error)


if __name__ == '__main__':
    print('Создание базы данных PostgreSQL...')
    create_db()
    print('Создание таблиц...')
    create_tables()
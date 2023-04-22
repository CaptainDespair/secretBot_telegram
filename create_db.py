import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import create_engine

from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE_NAME, PG_URL

from models import Base

engine = create_engine(PG_URL)

def create_db():
    try:
        connection = psycopg2.connect(user=PG_USER,
                                      password=PG_PASSWORD,
                                      host=PG_HOST,
                                      port=PG_PORT)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        cursor.execute(f'create database {PG_DATABASE_NAME}')
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
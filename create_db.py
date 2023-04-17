import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import create_engine

from models import Base
from config import POSTGRES_PASSWORD


def create_db():
    try:
        connection = psycopg2.connect(user="postgres",
                                    password=POSTGRES_PASSWORD,
                                    host="127.0.0.1",
                                    port="5432")
        
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute('create database secret_db')
        print('База данных создана успешно')
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
    except (Exception, Error) as error:
        print(error)
            

def create_tables():
    user = 'postgres'
    password = POSTGRES_PASSWORD
    host = '127.0.0.1'
    port = '5432'
    database = 'secret_db'

    db_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(db_url)

    try:
        Base.metadata.create_all(engine)
        print('Таблицы созданы успешно')
    except:
        print('Возникли ошибки')


if __name__ == '__main__':
    print('Создание базы данных PostgreSQL...')
    create_db()
    print('Создание таблиц...')
    create_tables()
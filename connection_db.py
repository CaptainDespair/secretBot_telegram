import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import POSTGRES_PASSWORD

def db_connection():
    try:
        connection = psycopg2.connect(user="postgres",
                                    password=POSTGRES_PASSWORD,
                                    host="127.0.0.1",
                                    port="5432",
                                    database="secret_db")
        
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print('Подключение успешно')
    except (Exception, Error) as error:
        print(error)
    finally:
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    db_connection()
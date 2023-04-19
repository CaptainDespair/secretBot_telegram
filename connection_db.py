import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import POSTGRES_PASSWORD
from create_db import user, host, port, database

def db_connection():
    try:
        connection = psycopg2.connect(user=user,
                                      password=POSTGRES_PASSWORD,
                                      host=host,
                                      port=port,
                                      database=database)
        
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
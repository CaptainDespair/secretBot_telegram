import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from configs.config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE_NAME

def db_connection():
    try:
        connection = psycopg2.connect(user=PG_USER,
                                      password=PG_PASSWORD,
                                      host=PG_HOST,
                                      port=PG_HOST,
                                      database=PG_DATABASE_NAME)
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
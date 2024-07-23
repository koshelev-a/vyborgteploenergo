import psycopg2
from psycopg2 import OperationalError
from connection_database import connection

def select_table(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result_select_query = cursor.fetchone()
        print("Найдены записи в таблице!\n", result_select_query)

    except OperationalError as e:
        print(f"The error '{e}' occurred")

    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL соединение закрыто")

select_table_query = 'select * from test_table' # Переменная запроса
select_table(connection, select_table_query) # Вызов функции

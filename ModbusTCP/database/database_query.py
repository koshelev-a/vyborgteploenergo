import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

# class connect_to_db:
#     def __init__(self):
#         self.connection = psycopg2.connect(
#             host = os.getenv("host_db"),
#             port = os.getenv("port_db"),
#             database = os.getenv("database_db"),
#             user = os.getenv("user_db"),
#             password = os.getenv("password_db")
#         )
class DataFetcher:
    def __init__(self):
        self.record = None
    
    def select_data(self, table, cod):
        try:
            connection = psycopg2.connect(
                host = os.getenv("host_db"),
                port = os.getenv("port_db"),
                database = os.getenv("database_db"),
                user = os.getenv("user_db"),
                password = os.getenv("password_db")
            )

            cursor = connection.cursor()
            sql_select_query = """SELECT val FROM public.tr%s WHERE cod = %s ORDER BY tm DESC LIMIT 1"""
            cursor.execute(sql_select_query, (table, cod))
            record = cursor.fetchone()
            self.record = record[0] if record else None

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
import psycopg2
import os
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Получение данных из .env файла
load_dotenv()

db_name = os.getenv('DB_TABLE')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        #Пытаемся подключиться к базе данных
        connection = psycopg2.connect(
                                database=db_name,
                                user=db_user, 
                                password=db_password,
                                host=db_host,
                                port=db_port)
        print("Вы подключены к - БД!\n")
    
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection(db_name, db_user, db_password, db_host, db_port)
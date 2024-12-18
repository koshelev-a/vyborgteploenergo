import os
import logging
import struct
import datetime
from time import sleep
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient
from database.database_query import DataFetcher

# Загрузка переменных окружения
load_dotenv()

class ModbusClient:
    def __init__(self, host, port):
        self.client = ModbusTcpClient(host, port=port)
        self.connect()

    def connect(self):
        return self.client.connect()

    def read_holding_registers(self, address, count):
        return self.client.read_holding_registers(address, count)

    def write_registers(self, address, registers):
        return self.client.write_registers(address, registers)

    def close(self):
        self.client.close()

def main():
    modbus_client = ModbusClient('localhost', os.getenv('port_client'))

    if not modbus_client.connect():
        print("Ошибка подключения к Modbus серверу")
        return 

    try:
        while True:
            # Извлечение данных из базы данных
            current_date = datetime.datetime.now().strftime('%d%m%Y') #Получения актуальной даты
            fetcher = DataFetcher()
            fetcher.select_data(int(current_date), 226)

            if fetcher.record is None:
                print("Нет данных для записи")
                continue
            
            try:
                packed_data = struct.pack('<f', fetcher.record)
            except Exception as e:
                print(f"Ошибка упаковки данных: {e}")
                continue

            registers = struct.unpack('<H', packed_data[2:])

            # Запись данных в регистры Modbus, начиная с адреса 1
            result = modbus_client.write_registers(1, registers)
            if result.isError():
                print("Ошибка записи регистров Modbus")
            else:
                print(f"Записанные регистры: {registers}")

            # Чтение регистров для проверки
            result = modbus_client.read_holding_registers(1, len(registers))
            if not result.isError():
                print(f"Регистры хранения: {result.registers}")
            else:
                print("Ошибка чтения регистров хранения")

            #print(f"Текущая дата: {current_date}, Полученные данные: {fetcher.record}, Упакованные данные: {packed_data}") #Для отладки данных

            sleep(30)  # Задержка перед следующим циклом "сек"

    finally:
        modbus_client.close()

if __name__ == "__main__":
    main()
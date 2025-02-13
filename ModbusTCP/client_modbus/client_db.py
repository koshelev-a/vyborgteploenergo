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
            current_date = datetime.datetime.now().strftime('%d%m%Y') # Получения актуальной даты
            array_cod = [258, 257, 259, 266, 260, 254, 255, 267, 262, 263, 264, 261, 268] # Перебераем коды устройств

            for cod in array_cod:
                fetcher = DataFetcher()
                fetcher.select_data(int(current_date), cod)  # Вызываем функцию с текущей датой и кодом
                print(f"Код: {cod}, Результат: {fetcher.record}")  # Вывод результата для текущего кода

            # Если данных нет, переходим к следующему коду
                if fetcher.record == 0:
                    print(f"Нет данных для записи для кода {cod}")
                    continue

                try:
                    packed_data = struct.pack('<f', fetcher.record)
                except Exception as e:
                    print(f"Ошибка упаковки данных для кода {cod}: {e}")
                    continue

                registers = struct.unpack('<HH', packed_data)  # Распаковка данных в два регистра

                # Запись данных в регистры Modbus, начиная с адреса 1
                result = modbus_client.write_registers(1, registers)
                if result.isError():
                    print(f"Ошибка записи регистров Modbus для кода {cod}")
                else:
                    print(f"Записанные регистры для кода {cod}: {registers}")

                # Чтение регистров для проверки
                result = modbus_client.read_holding_registers(1, len(registers))
                if not result.isError():
                    print(f"Регистры хранения для кода {cod}: {result.registers}")
                else:
                    print(f"Ошибка чтения регистров хранения для кода {cod}")

            sleep(30)  # Задержка перед следующим циклом "сек"

    finally:
        modbus_client.close()

if __name__ == "__main__":
    main()
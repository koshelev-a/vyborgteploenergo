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
    modbus_client = ModbusClient(os.getenv('host_client'), os.getenv('port_client'))

    if not modbus_client.connect():
        print("Ошибка подключения к Modbus серверу")
        return 

    try:
        while True:
            # Извлечение данных из базы данных
            current_date = datetime.datetime.now().strftime('%d%m%Y')  # Получение актуальной даты
            array_cod = [258, 257, 259, 260, 254, 256, 267, 268, 266, 269, 255, 262, 263, 264, 261]  #Перебираем коды устройств

            for index, cod in enumerate(array_cod):
                fetcher = DataFetcher()
                fetcher.select_data(current_date, cod)
                formatted_value = float("{:.2f}".format(fetcher.record))  # Вызываем функцию с текущей датой и кодом
                print(f"Код: {cod}, Результат: {formatted_value}")  # Вывод результата для текущего кода

                # Если данных нет, переходим к следующему коду
                if formatted_value == 0:
                    print(f"Нет данных для записи для кода {cod}")
                    continue

                try:
                    packed_data = struct.pack('<f', formatted_value)
                except Exception as e:
                    print(f"Ошибка упаковки данных для кода {cod}: {e}")
                    continue

                registers = struct.unpack('<H', packed_data[2:])[0] # Распаковка данных в два регистра

                # Устанавливаем адрес регистра равным текущему коду
                register_address = 1 + index  # Присваиваем register_address значение из array_cod

                # Запись данных в регистры Modbus
                result = modbus_client.write_registers(register_address, registers)
                if result.isError():
                    print(f"Ошибка записи регистров Modbus для кода {cod}")
                else:
                    print(f"Записанные регистры для кода {cod}: {registers} & Адрес регистра:{register_address}")

            sleep(30)  # Задержка перед следующим циклом "сек"

    finally:
        modbus_client.close()

if __name__ == "__main__":
    main()
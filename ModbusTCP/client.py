import os
import logging
from time import sleep
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient
from scada_passing import driver, url_address, sign_in, to_iframe, query_from_table
import struct

def main():
    print(f'Запускается парсер!')

    url_address(url= os.getenv('url_scada'))

    sign_in(login = os.getenv('login'), password = os.getenv('password'))

    sleep (3) #Пауза в 3 секунды

    to_iframe(idFrame="frameView")

    # Получение данных из .env файла
    load_dotenv()

    # Настройка логирования
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    # Настройка клиента
    client = ModbusTcpClient('localhost', port = os.getenv('port_client'))

    # Подключение к шлюзу
    if client.connect():
        try:
            while True:
                # Чтение 10 регистров хранения начиная с адреса 0
                result = client.read_holding_registers(1, 16)
                if not result.isError():
                    print(f"Регистры хранения: {result.registers}")
                else:
                     print("Ошибка чтения регистров хранения")
                
                # Получения значений с таблицы в массив для хранения значений float
                float_scada = []

                # Цикл для получения значений из таблицы
                for i in range(1, 17):  # от 1 до 17
                    tr_data = f"//table/tbody/tr[{i}]/td[2]"
                    float_value = query_from_table(trData=tr_data)
                    float_scada.append(float_value.replace(",", "."))  # Добавление значения в список

                # Вывод значений из float_scada для проверки
                print(float_scada)

                # Цикл для записи значений в регистры
                for i in range(len(float_scada)):
                    # Преобразование float значения в два 16-битных регистра в формате little-endian
                    float_value = float(float_scada[i])  # Преобразуем строку в float
                    packed_value = struct.pack('<f', float_value)  # '<f' означает little-endian формат для float
                    registers = struct.unpack('<H', packed_value[2:])[0]  # unpack в 2 16-битных регистра, выбран только 1 их них (старший)

                    # Запись в регистры
                    result = client.write_registers(i + 1, registers)

                    # Проверка результата записи
                    if result.isError():
                        print(f"Ошибка записи для регистра {i + 1}: {result}")
                    else:
                        print(f"Запись выполнена успешно в регистр {i + 1}!")

                #Задержка в 2 секунды
                sleep(2)

        finally:
            # Закрытие соединения
            client.close()
    else:
        print("Не удалось подключиться к шлюзу")
    

if __name__ == "__main__":
    main()
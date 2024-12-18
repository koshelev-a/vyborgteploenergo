import os
import logging
import struct
from time import sleep
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Загрузка переменных окружения
load_dotenv()

class WebDriver:
    def __init__(self):
        self.driver = self.create_driver()

    @staticmethod
    def create_driver():
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def url_address(self, url):
        self.driver.get(url)

    def sign_in(self, login, password):
        self._enter_text(By.ID, "txtUsername", login)
        self._enter_text(By.ID, "txtPassword", password, press_enter=True)

    def _enter_text(self, by, identifier, text, press_enter=False):
        element = self.driver.find_element(by, identifier)
        element.clear()
        element.send_keys(text)
        if press_enter:
            element.send_keys(Keys.RETURN)

    def to_iframe(self, idFrame):
        iframe = self.driver.find_element(By.ID, idFrame)
        self.driver.switch_to.frame(iframe)

    def query_from_table(self, trData):
        return self.driver.find_element(By.XPATH, trData).text

    def close(self):
        self.driver.quit()

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
    print(f'Запускается парсер!')
    web_driver = WebDriver()
    modbus_client = ModbusClient('localhost', os.getenv('port_client'))

    try:
        web_driver.url_address(url=os.getenv('url_scada'))
        web_driver.sign_in(login=os.getenv('login'), password=os.getenv('password'))
        sleep(3)
        web_driver.to_iframe(idFrame="frameView")

        while True:
            result = modbus_client.read_holding_registers(1, 16)
            if not result.isError():
                print(f"Регистры хранения: {result.registers}")
            else:
                print("Ошибка чтения регистров хранения")

            float_scada = []

            for i in range(1, 17):
                tr_data = f"//table/tbody/tr[{i}]/td[2]"
                float_value = web_driver.query_from_table(trData=tr_data)
                float_value = float_value.replace(" ", "").replace(",", ".")

                if float_value not in {None, "", "---"}:
                    try:
                        # Если value - число, оставляем его, иначе обрабатываем
                        if isinstance(float_value, (int, float)):
                            float_value = float(float_value)
                        else:
                            float_value = float(float(float_value.replace(" ", "").replace(",", ".")))
                    except ValueError:
                        print(f"Недопустимое значение: {float_value}")
                        float_value = 0
                else:
                    float_value = 0

                float_scada.append(float_value)

            print(float_scada)

            for i, value in enumerate(float_scada):
                packed_value = struct.pack('<f', value)
                registers = struct.unpack('<H', packed_value[2:])[0] 
                result = modbus_client.write_registers(i + 1, registers)

                if result.isError():
                    print(f"Ошибка записи для регистра {i + 1}: {result}")
                else:
                    print(f"Запись выполнена успешно в регистр {i + 1}!")

            sleep(2)

    finally:
        web_driver.close()
        modbus_client.close()

if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Получение данных из .env файла
load_dotenv()

options = Options()
options.headless = True  # Запуск в headless режиме
options.add_argument("--no-sandbox")  # Отключение песочницы, если есть проблемы с правами
options.add_argument("--disable-dev-shm-usage")  # Использование памяти непосредственно в системе

#Подключения к браузеру
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#Адрес подключения
def url_address(url):
    driver.get(url)

#Авторизация
def sign_in(login, password):
    #Вводим логин в окне авторизации
    search_login = driver.find_element(By.ID, "txtUsername")
    search_login.clear()
    search_login.send_keys(login)

    #Вводим пароль в окне авторизации
    search_password = driver.find_element(By.ID, "txtPassword")
    search_password.clear()
    search_password.send_keys(password)
    search_password.send_keys(Keys.RETURN)

#Перекоючает на фрейм
def to_iframe(idFrame):
    iframe = driver.find_element(By.ID, idFrame)
    driver.switch_to.frame(iframe)

#Получения данных из таблицы (Убранно навзание полей = "trName", оставлены только данные)
def query_from_table(trData): #trName,
    #name = driver.find_element(By.XPATH, trName).text #"//table/tbody/tr[2]/td[2]"
    data = driver.find_element(By.XPATH, trData).text #"//table/tbody/tr[2]/td[2]"

    return data
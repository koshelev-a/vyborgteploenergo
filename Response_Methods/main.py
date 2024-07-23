import os
import time
from dotenv import load_dotenv
from scada_passing import driver, url_address, sign_in, to_iframe, query_from_table

def main():
    print(f'Главный файл')

    url_address(url='http://46.175.215.84:8080/View')

    sign_in(login = os.getenv('login'), password = os.getenv('password'))

    time.sleep(3) #Пауза в 3 секунды

    to_iframe(idFrame="frameView")

    print(query_from_table(trName = "//table/tbody/tr[1]/td[1]/div/span[2]", trData = "//table/tbody/tr[1]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[2]/td[1]/div/span[2]", trData = "//table/tbody/tr[2]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[3]/td[1]/div/span[2]", trData = "//table/tbody/tr[3]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[4]/td[1]/div/span[2]", trData = "//table/tbody/tr[4]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[5]/td[1]/div/span[2]", trData = "//table/tbody/tr[5]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[6]/td[1]/div/span[2]", trData = "//table/tbody/tr[6]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[7]/td[1]/div/span[2]", trData = "//table/tbody/tr[7]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[8]/td[1]/div/span[2]", trData = "//table/tbody/tr[8]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[9]/td[1]/div/span[2]", trData = "//table/tbody/tr[9]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[10]/td[1]/div/span[2]", trData = "//table/tbody/tr[10]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[11]/td[1]/div/span[2]", trData = "//table/tbody/tr[11]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[12]/td[1]/div/span[2]", trData = "//table/tbody/tr[12]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[13]/td[1]/div/span[2]", trData = "//table/tbody/tr[13]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[14]/td[1]/div/span[2]", trData = "//table/tbody/tr[14]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[15]/td[1]/div/span[2]", trData = "//table/tbody/tr[15]/td[2]"))
    print(query_from_table(trName = "//table/tbody/tr[16]/td[1]/div/span[2]", trData = "//table/tbody/tr[16]/td[2]"))

    driver.close()

if __name__ == "__main__":
    main()
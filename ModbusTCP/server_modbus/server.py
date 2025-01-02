from dotenv import load_dotenv
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import os
import logging

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

host = os.getenv("host_srv")
port = os.getenv("port_srv")

# Создание хранилища данных
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [1]*100),
    co=ModbusSequentialDataBlock(0, [2]*100),
    hr=ModbusSequentialDataBlock(0, [3]*100),
    ir=ModbusSequentialDataBlock(0, [4]*100))

# Идентификация устройства
identity = ModbusDeviceIdentification()
identity.VendorName = 'VyborgTeploEnergo'
identity.ProductCode = 'MyProduct'
identity.VendorUrl = 'https://vyborgteploenergo.ru'
identity.ProductName = 'MyModbusServer'
identity.ModelName = 'Modbus Server'
identity.MajorMinorRevision = '1.0'

# Запуск сервера
StartTcpServer(context=ModbusServerContext(slaves=store, single=True), identity=identity, address=(host, port))

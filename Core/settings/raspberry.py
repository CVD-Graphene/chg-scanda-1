# from Core.utils import get_serial_port
#
#
# SERIAL_PORT = get_serial_port()
MAX_RECIPE_STEP_SECONDS = 60 * 60 * 24 * 2  # set to None for remove limit for step time

# ACCURATE_VAKUMETR_PORT = 1
ACCURATE_VAKUMETR_COMMUNICATOR_PORT = 1
# ACCURATE_VAKUMETR_USB_PORT = '/dev/ttyUSB1'  # FOR CVD-GRAPHENE USE USB1 (?)
ACCURATE_VAKUMETR_USB_PORT = '1-1.2.3.4'  # порт по usb (хаб или отдельно -- неважно),
# команда для определения: sudo dmesg | grep ttyUSB | grep usb
ACCURATE_VAKUMETR_BAUDRATE = 115200  # FOR CVD-GRAPHENE USE USB1 (?)

RRG_USB_PORT = '1-1.2.2'

# CURRENT_SOURCE_USB_PORT = '/dev/ttyUSB0'
CURRENT_SOURCE_USB_PORT = '1-1.2.3.1'
CURRENT_SOURCE_BAUDRATE = 9600
CURRENT_SOURCE_TIMEOUT = 0.05
# CURRENT_SOURCE_COMMUNICATOR_PORT = 3

# PYROMETER_TEMPERATURE_USB_PORT = '/dev/ttyUSB2'
PYROMETER_TEMPERATURE_USB_PORT = '1-1.2.4'
PYROMETER_TEMPERATURE_BAUDRATE = 19200

# BACK_PRESSURE_VALVE_USB_PORT = '/dev/ttyUSB3'
BACK_PRESSURE_VALVE_USB_PORT = '1-1.4.1.3'  # Mb pyrometr
BACK_PRESSURE_VALVE_BAUDRATE = 9600

BH_RRG_CONTROLLER_USB_PORT = '/dev/ttyACM0'
BH_RRG_CONTROLLER_BAUDRATE = 38400
BH_RRG_CONTROLLER_MAX_RRG_VOLTAGE = 5.0

AIR_VALVE_CONFIGURATION = {
    'PORT': 25, "NAME": "Air",
}
AIR_VALVE_NAME = AIR_VALVE_CONFIGURATION['NAME']

PUMP_CONFIGURATION = {
    'MANAGE_PORT': 3,  # порт управления (вкл/выкл)
    'VALVE_PORT': 2,  # открыть/закрыть клапан перед насосом. needle valve has adress gpio12
    "NAME": 'Pump',
}

MAX_DEFAULT_SCCM_VALUE = 200

RRG_SPI_READ_CHANNEL = 0
RRG_SPI_WRITE_CHANNEL = 1
RRG_SPI_SPEED = 20000
RRG_SPI_READ_DEVICE = 1  # Potential vakumetr port
RRG_SPI_WRITE_DEVICE = 0  # ONLY 0 because we have only one instrument for write using spi

VAKUMETR_SPI_READ_CHANNEL = 0
VAKUMETR_SPI_SPEED = 20000
VAKUMETR_SPI_READ_DEVICE = 0

DIGITAL_FUSE_PORTS = [5, 22, 6, ]

VALVES_CONFIGURATION = [
    # {
    #     "NAME": "NO GAS",
    #     'PORT': 12,  # GPIO PORT FOR RELE
    #     "IS_GAS": True,
    #     "MAX_SCCM": 2175.0,  # NOT NECESSARY, IF NOT PROVIDED, WILL BE USED `MAX_DEFAULT_SCCM_VALUE`
    #     # 'CONTROLLER_VOLTAGE_RATIO': 1,  # BH CONTROLLER VOLTAGE FUNCTION ('a' from 'a*x+b') (0, +inf)
    #     # 'CONTROLLER_VOLTAGE_SHIFT': 0,  # BH CONTROLLER VOLTAGE FUNCTION ('b' from 'a*x+b') (-inf, +inf)
    #     # 'ADDRESS': 0,  # RRG ADDRESS FOR SPI (from 0 to 7: 000, 001, ..., 111)
    #     # 'DAC_ADDRESS': 0,  # RRG ADDRESS FOR SPI DAC [SET VALUE] (from 0 to 7: 000, 001, ..., 111)
    #     'VAKUMETR_ADDRESS': 0,  # VAKUMETR ADDRESS FOR READING PRESSURE IN BALLOON
    #     "INSTRUMENT_NUMBER": 3,  # rrg modbus instrument number
    # },
    {
        "NAME": "Ar",
        'PORT': 18,  # GPIO PORT FOR RELE
        "IS_GAS": True,
        "MAX_SCCM": 2175.0,  # NOT NECESSARY, IF NOT PROVIDED, WILL BE USED `MAX_DEFAULT_SCCM_VALUE`
        'VAKUMETR_ADDRESS': 0,  # VAKUMETR ADDRESS FOR READING PRESSURE IN BALLOON
        "INSTRUMENT_NUMBER": 3,  # rrg modbus instrument number
    },
    {
        'PORT': 24, "NAME": "CH_4", "IS_GAS": True,
        # 'CONTROLLER_VOLTAGE_RATIO': 1, 'CONTROLLER_VOLTAGE_SHIFT': 0,
        # 'ADDRESS': 1, 'DAC_ADDRESS': 1,
        'MAX_SCCM': 43.2,
        'VAKUMETR_ADDRESS': 1,  # VAKUMETR ADDRESS FOR READING PRESSURE IN BALLOON
        "INSTRUMENT_NUMBER": 1,  # rrg modbus instrument number
    },
    {
        'PORT': 23, "NAME": "H_2", "IS_GAS": True,
        # 'CONTROLLER_VOLTAGE_RATIO': 1, 'CONTROLLER_VOLTAGE_SHIFT': 0,
        # 'ADDRESS': 4, 'DAC_ADDRESS': 7,
        'MAX_SCCM': 606.0,
        "VAKUMETR_ADDRESS": 2,  # VAKUMETR ADDRESS FOR READING PRESSURE IN BALLOON
        "INSTRUMENT_NUMBER": 2,  # rrg modbus instrument number
    },
]

ALL_GPIO_VALVES_CONFIG = VALVES_CONFIGURATION + \
                         [AIR_VALVE_CONFIGURATION] + \
                         [PUMP_CONFIGURATION]

# VALVE_LIST = list(map(lambda x: x.get('NAME'), VALVES_CONFIGURATION))
VALVE_LIST = list(map(lambda x: x.get('NAME'), ALL_GPIO_VALVES_CONFIG))
# GAS_LIST = list(map(lambda x: x.get('NAME'), filter(lambda x: x.get("IS_GAS", False), VALVES_CONFIGURATION)))
GAS_LIST = list(map(lambda x: x.get('NAME'), VALVES_CONFIGURATION))

TABLE_COLUMN_NAMES = ["Процесс", "Аргумент 1", "Аргумент 2", "Аргумент 3", "Комментарий"]

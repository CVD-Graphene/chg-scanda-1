import time

import serial

RS485 = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.001
)


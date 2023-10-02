
try:
    import wiringpi
except:
    pass
import serial
from time import sleep
import codecs

from coregraphene.utils.algorithms import crc16
from .ports import get_serial_port
print("SERIAL:", get_serial_port())

PORT = "/dev/ttyUSB1"
#  '/dev/ttyAMA0'

def f(i):
    return str(hex(i))[2:].upper()

def crc16x(data: str, poly: hex = 0xA001) -> str:
    '''
        CRC-16 MODBUS HASHING ALGORITHM
    '''
    crc = 0xFFFF
    for byte in data:
        crc ^= ord(byte)
        for _ in range(8):
            crc = ((crc >> 1) ^ poly
                   if (crc & 0x0001)
                   else crc >> 1)

    hv = hex(crc).upper()[2:]
    blueprint = '0000'
    return blueprint if len(hv) == 0 else blueprint[:-len(hv)] + hv


def test_rrg_1():
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen(PORT, 115200)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    # for i in '1':
        # sleep(1)
    # SEND_STR = f'0010MV00D\r'
    command = f"02030001"
    # command += crc16x(command)
    # command = f"02030001"
    hi, lo = crc16(codecs.decode(command, "hex"))  # CRC = b'\x58\x7A'

    # print("!!!!!!!!!! {0:02X} {1:02X}".format(hi, lo))
    # print("ALL COMM:", s + f(lo) + f(hi))
    command += f(lo) + f(hi)
    # byte_command = bytearray(command.encode("ASCII")) # + bytes([hi, lo])
    byte_command = codecs.decode(command, "hex")  # + bytes([hi, lo])
    # serial = wiringpi.serialOpen('/dev/ttyACM0', 9600)  # Requires device/baud and returns an ID
    ans = wiringpi.serialPuts(serial, command)  # ONLY STR!!!!!
    # print("Answer:", ans)
    # b = ""
    counter = 0
    # sleep(1)
    while True:
        b = wiringpi.serialGetchar(serial)
        counter += 1
        if counter > 100 or b is None or b == -1:
            print(b, end='|')
            break
    print('')
    wiringpi.serialClose(serial)


def test_2():

    RS485 = serial.Serial(
        # port='/dev/ttyAMA0',
        port=PORT,
        writeTimeout=0,
        write_timeout=0,
        baudrate=115200,
        # baudrate=9600,
        # parity=serial.PARITY_NONE,
        # stopbits=serial.STOPBITS_ONE,
        # bytesize=serial.EIGHTBITS,
        timeout=0.001,
    )

    # command = f"02030001"
    # hi, lo = crc16(codecs.decode(command, "hex"))
    # command += f(lo) + f(hi)
    # byte_command = codecs.decode(command, "hex")

    while True:
        # n = 2
        # command = f"00{n}030001"
        command = f"02030001"
        hi, lo = crc16(codecs.decode(command, "hex"))  # CRC = b'\x58\x7A'

        # print("!!!!!!!!!! {0:02X} {1:02X}".format(hi, lo))
        # print("ALL COMM:", s + f(lo) + f(hi))
        command += f(lo) + f(hi)
        # command += "F38B"
        # byte_command = bytearray(command.encode("ASCII")) # + bytes([hi, lo])
        byte_command = codecs.decode(command, "hex")  # + bytes([hi, lo])
        # byte_command = b'\x02\x03\x00\x01\x5C\x30'
        # print("GGG", b'0010MV0' + bytes([hi, lo]))
        # command += crc
        print("|>> COMMAND:", command, byte_command)
        # RS485.write(bytearray(command.encode("ASCII")))
        RS485.write(byte_command)
        sleep(0.1)
        x = RS485.readline()
        print(x)
        sleep(1)

import time

import serial

from crc import CrcCalculator, Crc8


def test_rrg_3():

    RS485 = serial.Serial(
        port=PORT,
        baudrate=19200,
        # writeTimeout=0,
        # write_timeout=0,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.05,
    )

    while True:
        n = 1
        #command = bin(int('01030002000265CB', base=16))[2:]
        command = bytes.fromhex('01030002000265CB')
        #command = bytearray("01030002000265CB")
        #command = (1000).to_bytes(2, byteorder='big')
        #command = bytearray("0010MV00D\r".encode("ASCII"))
        print("command:", command)
        RS485.write(command)
        time.sleep(1)
        in_wait = RS485.inWaiting()
        print("In waiting:", in_wait)
        r = b''
        while RS485.inWaiting() > 0:
            ReceivedData = RS485.readline()
            r += ReceivedData

        print("RECEIVED DATA:", r)

        # ReceivedData = RS485.readline()
        # print("received:", ReceivedData)
        time.sleep(1)


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        # test_3()
        # test_2()
        test_rrg_3()
        # test_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")

# from Tests.devices.ports import get_serial_port
import time

try:
    import wiringpi
except:
    pass

try:
    import spidev
except Exception as e:
    print("Spidev import error:", e)
# import serial
from time import sleep
# import codecs


def test_rough_vakumetr_1():
    SPIchannel = 0
    SPIspeed = 100000
    wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)
    send_data = b'000'
    while True:
        receive_data = wiringpi.wiringPiSPIDataRW(SPIchannel, send_data)
        print("|> Receive:", receive_data)
        sleep(1)

import string
digs = string.digits + string.ascii_letters


def int2base(x, base=2):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x = x // base

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


# WORK VERSION
def test_rough_vakumetr_2():
    SPIchannel = 0
    SPIspeed = 20000
    spi = spidev.SpiDev()
    spi.open(SPIchannel, 0)  # 0,1 - выбор чипа (ррг и вакуметры)
    spi.max_speed_hz = SPIspeed
    print("Connected!")
    spi.lsbfirst = False
    print("spi.lsbfirst = " + str(spi.lsbfirst))
    spi.bits_per_word = 8
    spi.mode = 0b01
    print("spi.mode = " + str(spi.mode))
    spi.cshigh = False
    print("spi.cshigh = " + str(spi.cshigh))

    txData = [0x80, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
    while True:
        # txData = [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
        txData = [0x80, 0xFF, 0x00, 0x00]
        rxData = spi.xfer(txData)
        print("Receive:", rxData)
        print("Receive:", end=' ')
        if len(rxData) >= 3:
            s = ''.join(map(lambda x: int2base(x).zfill(8), rxData[:4]))
            n = int(s[8:18], 2)
            print(n)  #, s, s[8:18])
        sleep(1)

    spi.close()


# TEST ЦАП
def test_rough_vakumetr_3():
    SPIchannel = 1
    SPIspeed = 20000
    spi = spidev.SpiDev()
    spi.open(SPIchannel, 0)  # 0 - выбор чипа
    spi.max_speed_hz = SPIspeed
    print("Connected!")
    spi.lsbfirst = False
    print("spi.lsbfirst = " + str(spi.lsbfirst))
    spi.bits_per_word = 8
    # spi.mode = 0b01
    print("spi.mode = " + str(spi.mode))
    spi.cshigh = False
    print("spi.cshigh = " + str(spi.cshigh))

    txData = [0b11110000, 0b00000000]  # DAC data  and control reset
    rxData = spi.xfer(txData)
    sleep(0.5)
    txData = [0b10100000, 0b00000000]  # LDAC LOW
    rxData = spi.xfer(txData)
    sleep(0.5)
    txData = [0b10000000, 0b00001111]  # range 0 to Vref
    rxData = spi.xfer(txData)
    sleep(0.5)

    txData = [0x80, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
    while True:
        txData = [0b00011001, 0b11101001]  # send to chB
        print("Send to spi:", txData)
        rxData = spi.xfer(txData)

        print("Receive:", rxData)

        sleep(0.25)
        # s = '0000010000000000'
        # # txData = [int(s, 2)]
        # txData = [0x01, 0x00]
        # txData = [0x80, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
        # rxData = spi.xfer(txData)
        # print("Receive:", rxData)
        # print("Receive:", end=' ')
        # if len(rxData) >= 3:
        #     s = ''.join(map(lambda x: int2base(x).zfill(8), rxData[:4]))
        #     n = int(s[8:18], 2)
        #     print(n) #, s, s[8:18])
        # sleep(0.01)

    spi.close()


def test_writing():
    start = time.time()
    filename = "test1.txt"
    with open(filename, 'w') as file:
        for i in range(1000000):
            file.write(str(i)+'\n')
    time2 = time.time()
    print("Time:", time2 - start)
    arr = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                arr.append(int(line))
    print("Time read:", time.time() - time2)


if __name__ == "__main__":
    print("TEST 1 ===>")
    # test_rough_vakumetr_3()
    try:
        test_writing()
        # test_rough_vakumetr_3()  # WORK VERSION
        # test_rough_vakumetr_3()
        s = '0000010000000000'
        s = '1000100000000000'  # MAX VALUE
        # h = int2base(int(s, 2), base=16)
        # h = int(hex(int(s, 2)), 16)
        h = int(s, 2)
        print(h, type(h), type(0x44))
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")

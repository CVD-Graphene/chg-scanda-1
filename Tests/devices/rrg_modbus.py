import minimalmodbus as mm
import time


rrg = mm.Instrument('/dev/ttyUSB3', 1) #rrg 1 & 3 avaliable, H2 - 2
rrg.serial.baudrate = 19200
rrg.serial.timeout = 0.2
rrg.mode = mm.MODE_RTU
registervalue = rrg.read_register(2)


bit0 = (registervalue & 0b00000001) > 0
bit1 = (registervalue & 0b00000010) > 0
bit2 = (registervalue & 0b00000100) > 0
bit3 = (registervalue & 0b00001000) > 0
bit4 = (registervalue & 0b00010000) > 0
bit5 = (registervalue & 0b00100000) > 0
bit6 = (registervalue & 0b01000000) > 0
bit7 = (registervalue & 0b10000000) > 0
print(bit0)
print(bit1)
print(bit2)
print(bit3)
print(bit4)
print(bit5)
print(bit6)
print(bit7)

#print(rrg.read_register(2))
#rrg.write_register(2, 19, functioncode=6)
#print(rrg.read_register(2))
while True:
    print(rrg.read_register(5))  # чтение расхода
    time.sleep(0.5)
    #rrg.write_register(4, 1, functioncode=6)  # задание расхода , functioncode=6 -- lля записи
    #print(rrg.read_register(4))  # чтение заданного расхода
    #print(rrg.read_register(5))  # чтение расхода


###############################################################

import minimalmodbus as mm
import time

rrg = mm.Instrument('/dev/ttyUSB1', 1)  # rrg 1 - канал ррг (0 1 2 3...)
rrg.serial.baudrate = 19200
rrg.serial.timeout = 0.2
rrg.mode = mm.MODE_RTU
# rrg.write_bits(2, 2, functioncode=15)

while True:
    try:
        # print(rrg.read_bit(2, number_of_bits=8, functioncode=15))
        registervalue = rrg.read_register(2)  # 2 - это что-то физическое из мануала
        print(registervalue)

        # тут 3 и 2 биты выставляются нулевыми для флагов
        bit2 = (registervalue & 0b00000010) > 0
        print(bit2)
        bit3 = (registervalue & 0b00000100) > 0
        print(bit3)
        # bits = 0b00000100
        # rrg.write_register(2, bits, 6)

    except IOError:
        print('Failed')

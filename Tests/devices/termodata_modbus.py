"""
Termodat
"""

import minimalmodbus as mm
import time

rrg = mm.Instrument('/dev/ttyUSB1', 1, debug=False)  # termodat  # 1-instrument of termodata (we have 3) 1 2 3
rrg.serial.baudrate = 9600
rrg.serial.timeout = 0.2
rrg.mode = mm.MODE_ASCII

reg = 377
reg1 = 384  # - on/off
REG_ON_OFF = 384

par = 0.00  # 0 -- off, 0.01 -- on
ON = 1  # 0.01
OFF = 0
TARGET_POINT = 0.0  # TARGET DEGREE

rrg.write_register(REG_ON_OFF, 0.0, 2)  # ON/OFF
print("on/off: " + str(rrg.read_register(reg1, 2)))
rrg.write_register(371, 1.0, 1)  # 50.5 degree  # /= 10 from real (want 100C - need 10.0)

READ_TARGET_1 = 369  # 171h *= 10 (10.0 is 100C)
READ_TARGET_2 = 48  # 30h *= 10
SPEED_REG = 377

rrg.write_register(REG_ON_OFF, OFF, 2)  # ON/OFF

"""
print("Tmax = " + str(int(str(rrg.read_register(371, 2)).replace('.',''))/10)) # - ystavka
rrg.write_register(REG_ON_OFF, OFF, 2)
print("on/off: " + str(rrg.read_register(reg1, 2)))
print("T = " + str(int(str(rrg.read_register(368, 2)).replace('.',''))/10))

rrg.write_register(371, TARGET_POINT, 2) #50.5 degree
time.sleep(1)
print("Tmax = " + str(int(str(rrg.read_register(371, 2)).replace('.',''))/10)) # - ystavka
print("Tmax = " + str(rrg.read_register(371, 2))) # - ystavka
print("Tmax2 = " + str(rrg.read_register(549, 2))) 
print("Tmax3 = " + str(rrg.read_register(369, 2))) 




print("on/off: " + str(rrg.read_register(reg1, 2)))
print("T = " + str(int(str(rrg.read_register(368, 2)).replace('.',''))/10))


rrg.write_register(352, 0, 2) #50 degree
rrg.write_register(379, 0, 2) #50 degree
print("program = " +str(rrg.read_register(545, 2)))

rrg.write_register(353, 0, 2) #50 degree
rrg.write_register(380, 0, 2) #50 degree
print("step = " +str(rrg.read_register(546, 2)))

rrg.write_register(354, 0, 2) #50 degree
print("step type = " +str(rrg.read_register(547, 2)))

print("time ostalos = " +str(rrg.read_register(548, 2)))

rrg.write_register(356, 0, 2) #50 degree
print("Tmax = " + str(int(str(rrg.read_register(549, 2)).replace('.',''))/10))


rrg.write_register(355, 0, 2) #50 degree
print("V = " + str(int(str(rrg.read_register(560, 2)).replace('.',''))/10))

rrg.write_register(reg1, par, 2)
print("on/off: " + str(rrg.read_register(reg1, 2)))
"""

for i in range(500):
    # print("T = " + str(int(str(rrg.read_register(368, 2)).replace('.',''))/10))
    print("T = " + str(rrg.read_register(368, 1)) + " | " + str(rrg.read_register(READ_TARGET_1, 1)) + " | " + str(
        rrg.read_register(READ_TARGET_2, 2)))
    # print("Tmax = " + str(int(str(rrg.read_register(549, 2)).replace('.',''))/10))
    time.sleep(0.5)





# from Tests.devices.ports import get_serial_port

try:
    import wiringpi
    import spidev
except:
    pass
# import serial
from time import sleep
# import codecs


def test_rele_1():
    channel = 7
    wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering
    wiringpi.wiringPiSetup()  # For sequential pin numbering
    wiringpi.pinMode(channel, 1)  # Set pin 6 to 1 ( OUTPUT )
    send = 1  # 1 - closed, 0 - opened
    while True:
        wiringpi.digitalWrite(channel, send)  # Write 1 ( HIGH ) to pin 6
        receive_data = wiringpi.digitalRead(channel)  # Read pin 6
        print("|> Receive:", receive_data, "| send:", send)
        send = 0 if send else 1
        sleep(0.5)


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        test_rele_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")

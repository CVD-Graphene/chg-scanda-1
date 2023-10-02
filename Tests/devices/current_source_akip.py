# from .ports import get_serial_port

try:
    import wiringpi
except:
    pass
import serial
from time import sleep


# PORT = get_serial_port()
PORT = "/dev/ttyUSB1"
#  '/dev/ttyAMA0'


def get_port():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    portList = []
    print("ALL PORTS:")
    for onePort in ports:
        portList.append(str(onePort))
        print(str(onePort))

    for onePort in ports:
        p = str(onePort)
        try:
            f = p.split('-')[0].strip()
            if f.find('USB') >= 0:
                return f
        except:
            continue
        # portList.append(str(onePort))
        # print(str(onePort))
    return "/dev/ttyUSB0"


def test_akip_2():
    # get_port()
    # return

    RS485 = serial.Serial(
        # port='/dev/ttyAMA0',
        # port=get_port(),
        port=PORT,
        # writeTimeout=0,
        # write_timeout=0,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.001,
    )
    ADDRESS = 3
    command_remote = f"A00{ADDRESS}SYSTem:REMote;\n"
    remote = f"SYST:REM"
    output_cmd = lambda x: f"OUTP {x}"
    command_beep_on = f"A00{ADDRESS}SYST:BEEP 1;\n"
    command_beep_off = f"A00{ADDRESS}SYST:BEEP 0;\n"

    command_measure_current = f"A00{ADDRESS}MEASure:CURRent?;\n"  # 10-4-32
    command_measure_voltage = f"A00{ADDRESS}MEASure:VOLTage?;\n"  # 10-4-31

    command_set_voltage = f"A00{ADDRESS}SOURce:VOLTage 30;\n"  # 10-4-34 // 30V
    command_get_voltage = f"A00{ADDRESS}SOURce:VOLTage?;\n"  # 10-4-35

    command_set_current = f"A00{ADDRESS}SOURce:CURRent 1;\n"  # 10-4-40
    command_get_current = f"A00{ADDRESS}SOURce:CURRent?;\n"  # 10-4-41

    command_get_errors = f"A00{ADDRESS}SYSTem:ERRor?;\n"  #

    def create_command(c):
        return f"A00{ADDRESS}{c};\n"

    def run_command(command):
        RS485.write(bytearray(command.encode("ASCII")))
        timeout = 0.05
        sleep(timeout)
        _answer = RS485.readline()
        command_get_errors = f"A00{ADDRESS}SYST:ERR?;\n"
        RS485.write(bytearray(command_get_errors.encode("ASCII")))
        sleep(timeout)
        _errors = RS485.readline()
        print(f"[COMMAND] {command.strip()}. Answer: {_answer} | Status: {_errors}")
        return _answer, _errors
        # print("ANSWER:", x)

    # max_voltage_limit = "SOURce:VOLTage:PROTection:LEVel 13.75"  # 10-4-36 Max voltage limit
    max_voltage_limit = "SOUR:VOLT:PROT:LEV 13.75"  # 10-4-36 Max voltage limit
    zero_voltage_limit = "SOUR:VOLT:PROT:LEV 0"  # 10-4-36 Max voltage limit
    # max_current_limit = "SOURce:CURRent:PROTection:LEVel 132"  # 10-4-43 Max current limit
    max_current_limit = "SOUR:CURR:PROT:LEV 132"  # 10-4-43 Max current limit
    zero_current_limit = "SOUR:CURR:PROT:LEV 0"  # 10-4-43 Max current limit
    # max_voltage_actual = "SOURce:VOLTage 13.12"  # 10-4-34 Voltage limit for actual value
    max_voltage_actual = "SOUR:VOLT 13.12"  # 10-4-34 Voltage limit for actual value
    zero_voltage_actual = "SOUR:VOLT 0"  # 10-4-34 Voltage limit for actual value
    # max_current_actual = "SOURce:CURRent 1.0"  # 10-4-40 Current limit for actual value
    max_current_actual = "SOUR:CURR 1.0"  # 10-4-40 Current limit for actual value
    zero_current_actual = "SOUR:CURR 0"  # 10-4-40 Current limit for actual value

    SLEEP_TIME = 1
    command_remote = create_command(remote)
    answer, errors = run_command(command_remote)
    answer, errors = run_command(create_command(output_cmd(1)))
    sleep(SLEEP_TIME)
    answer, errors = run_command(create_command(max_voltage_limit))
    sleep(SLEEP_TIME)
    answer, errors = run_command(create_command(max_current_limit))
    sleep(SLEEP_TIME)
    answer, errors = run_command(create_command(max_voltage_actual))
    sleep(SLEEP_TIME)
    answer, errors = run_command(command_get_voltage)
    print("|> CURRENT VOLTAGE:", answer)
    sleep(SLEEP_TIME)
    try:
        while True:
            # answer, errors = run_command(create_command(max_current_actual))
            answer, errors = run_command(command_get_current)
            print("|> CURRENT ACTUAL:", answer)
            sleep(SLEEP_TIME)
    except BaseException:
        answer, errors = run_command(create_command(zero_current_actual))
        answer, errors = run_command(create_command(zero_voltage_actual))
        # answer, errors = run_command(create_command(zero_current_limit))
        # answer, errors = run_command(create_command(zero_voltage_limit))
        answer, errors = run_command(create_command(output_cmd(0)))


if __name__ == "__main__":
    print("TEST 1 ===>")
    # try:
    test_akip_2()
    # test_1()
    print("TEST 1 ===> PASSED")
    # except Exception as e:
    #     print("[ERROR]", e)
    #     print("TEST 1 ===> FAILED")

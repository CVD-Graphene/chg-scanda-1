import time

from coregraphene.actions import AppAction, ValveListArgument, GasListArgument, SccmArgument, TimeEditArgument, \
    FloatArgument, IntKeyArgument, FloatKeyArgument, get_total_seconds_from_time_arg
from coregraphene.actions.exceptions import NotAchievingActionGoal
from coregraphene.conf import settings

# from coregraphene.recipe.exceptions import NotAchievingActionGoal


ACTIONS_NAMES = settings.ACTIONS_NAMES
TABLE_ACTIONS_NAMES = settings.TABLE_ACTIONS_NAMES
MAX_RECIPE_STEP_SECONDS = settings.MAX_RECIPE_STEP_SECONDS


def get_gas_index_by_name(name):
    for i, gas in enumerate(settings.VALVES_CONFIGURATION):
        if gas['NAME'] == name:
            return i


class PauseAction(AppAction):
    name = TABLE_ACTIONS_NAMES.PAUSE
    key = ACTIONS_NAMES.PAUSE
    args_info = [TimeEditArgument]

    def do_action(self, seconds):  # , *args, **kwargs):
        # print("SLEEP SECONDS:", seconds, time.time())
        start = time.time()
        while time.time() - start < seconds:
            time.sleep(1)
            self.interrupt_if_stop_state()


class TurnOnPumpAction(AppAction):
    name = TABLE_ACTIONS_NAMES.TURN_ON_PUMP
    key = ACTIONS_NAMES.TURN_ON_PUMP

    def do_action(self):
        self.system.change_pump_manage_active_effect(True)


class TurnOffPumpAction(AppAction):
    name = TABLE_ACTIONS_NAMES.TURN_OFF_PUMP
    key = ACTIONS_NAMES.TURN_OFF_PUMP

    def do_action(self):
        self.system.change_pump_manage_active_effect(False)


class OpenValveAction(AppAction):
    name = TABLE_ACTIONS_NAMES.OPEN_VALVE
    key = ACTIONS_NAMES.OPEN_VALVE
    args_info = [ValveListArgument]

    def do_action(self, valve_name: str):
        is_gas = valve_name in list(map(lambda x: x['NAME'], settings.VALVES_CONFIGURATION))
        is_air = valve_name == settings.AIR_VALVE_CONFIGURATION['NAME']
        if is_air:
            self.system.change_air_valve_opened(True)
        elif is_gas:
            index = get_gas_index_by_name(valve_name)
            self.system.change_gas_valve_opened(True, device_num=index)
        else:
            self.system.change_pump_valve_opened_effect(True)


class CloseValveAction(AppAction):
    name = TABLE_ACTIONS_NAMES.CLOSE_VALVE
    key = ACTIONS_NAMES.CLOSE_VALVE
    args_info = [ValveListArgument]

    def do_action(self, valve_name: str):
        is_gas = valve_name in list(map(lambda x: x['NAME'], settings.VALVES_CONFIGURATION))
        is_air = valve_name == settings.AIR_VALVE_CONFIGURATION['NAME']
        if is_air:
            self.system.change_air_valve_opened(False)
        elif is_gas:
            index = get_gas_index_by_name(valve_name)
            self.system.change_gas_valve_opened(False, device_num=index)
        else:
            self.system.change_pump_valve_opened_effect(False)


class CloseAllValvesAction(AppAction):
    name = TABLE_ACTIONS_NAMES.CLOSE_ALL_VALVES
    key = ACTIONS_NAMES.CLOSE_ALL_VALVES

    def do_action(self):
        self.system.change_air_valve_opened(False)

        for i, _ in enumerate(settings.VALVES_CONFIGURATION):
            self.system.change_gas_valve_opened(False, device_num=i)

        self.system.change_pump_valve_opened_effect(False)


class SetThrottlePercentAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_THROTTLE_PERCENT
    key = ACTIONS_NAMES.SET_THROTTLE_PERCENT
    args_info = [IntKeyArgument]

    def do_action(self, target_percent: int):
        self.system.back_pressure_valve_controller.set_target_percent(target_percent)


class FullOpenThrottleAction(AppAction):
    name = TABLE_ACTIONS_NAMES.FULL_OPEN_THROTTLE
    key = ACTIONS_NAMES.FULL_OPEN_THROTTLE
    args_info = []

    def do_action(self):
        self.system.back_pressure_valve_controller.on_full_open()


class FullCloseThrottleAction(AppAction):
    name = TABLE_ACTIONS_NAMES.FULL_CLOSE_THROTTLE
    key = ACTIONS_NAMES.FULL_CLOSE_THROTTLE
    args_info = []

    def do_action(self):
        self.system.back_pressure_valve_controller.on_full_close()


class SetThrottlePressureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_THROTTLE_PRESSURE
    key = ACTIONS_NAMES.SET_THROTTLE_PRESSURE
    args_info = [FloatKeyArgument]

    def do_action(self, target_pressure: float):
        self.system.back_pressure_valve_controller.turn_on_regulation(target_pressure)


class SetRrgSccmValueAction(AppAction):
    """
    Установить значение sccm для ррг
    """
    name = TABLE_ACTIONS_NAMES.SET_RRG_VALUE
    key = ACTIONS_NAMES.SET_RRG_VALUE
    args_info = [GasListArgument, SccmArgument]

    def do_action(self, valve_name: str, sccm: float):
        index = get_gas_index_by_name(valve_name)
        self.system.set_target_rrg_sccm_effect(sccm, device_num=index)


class SetRrgSccmValueWithPauseAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_RRG_VALUE_WITH_PAUSE
    key = ACTIONS_NAMES.SET_RRG_VALUE_WITH_PAUSE
    args_info = [GasListArgument, SccmArgument, TimeEditArgument]

    def do_action(self, valve_name: str, sccm: float, seconds: int):
        action_rrg = self.sub_action(SetRrgSccmValueAction)
        action_rrg.action(valve_name, sccm)

        action_pause = self.sub_action(PauseAction)
        action_pause.action(seconds)


class PumpOutCameraAction(AppAction):
    """
    1) закрываются все клапаны
    2) отправляется команда на клапан обратного давления открыться на 13%
    3) включается насос
    4) ожидаем наступления давления 10мбар
    5) открывает большой клапан на насос
    6) отправляет на клапан обратного давления команду полностью закрыться
    7) ожидаем наступления давления 10^-3 мбар
    8) закрываем все клапаны
    """
    name = TABLE_ACTIONS_NAMES.PUMP_OUT_CAMERA
    key = ACTIONS_NAMES.PUMP_OUT_CAMERA
    # args_info = [FloatArgument, TimeEditArgument]
    args_info = []

    def do_action(self):

        # 1 - закрываются все клапаны
        close_valves = self.sub_action(CloseAllValvesAction)
        close_valves.action()

        # 2 - отправляется команда на клапан обратного давления открыться на 13%
        throttle_percent = self.sub_action(SetThrottlePercentAction)
        throttle_percent.action(13.0)

        # 3 - включается насос
        turn_on_pump = self.sub_action(TurnOnPumpAction)
        turn_on_pump.action()

        # 4 - ожидаем наступления давления 10 мбар
        while self.system.get_accurate_vakumetr_value() >= 10.0:
            self.interrupt_if_stop_state()

            time.sleep(0.1)

            delta_time = time.time() - self.start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Откачка не завершилась до достижения максимального времени")
                raise NotAchievingActionGoal

        # 5 - открывает большой клапан на насос
        open_pump = self.sub_action(OpenValveAction)
        open_pump.action("Pump")

        # 6 - отправляет на клапан обратного давления команду полностью закрыться
        close_throttle = self.sub_action(FullCloseThrottleAction)
        close_throttle.action()

        # 7 - ожидаем наступления давления 10^-3 мбар
        while self.system.get_accurate_vakumetr_value() >= 0.001:
            self.interrupt_if_stop_state()
            # if self._is_stop_state():
            #     return
            time.sleep(0.1)

            delta_time = time.time() - self.start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Откачка не завершилась до достижения максимального времени")
                raise NotAchievingActionGoal

        # 8 - закрываются все клапаны
        close_valves = self.sub_action(CloseAllValvesAction)
        close_valves.action()


class VentilateCameraAction(AppAction):
    """
    1) Ток через фольгу постепенно уменьшается до 0
    2) на все ррг команда на ноль
    3) закрываются все клапаны
    4) на клапан обратного давления команда полностью закрыть
    5) ожидаем 30 секунд пока всё точно остынет
    6) включается ррг аргона
    7) открываем клапан аргона
    8) ожидаем пока давление не станет 950 мбар
    9) ожидаем 30 сек
    10) на ррг аргона команда на ноль
    11) закрываем клапан аргона
    """
    name = TABLE_ACTIONS_NAMES.VENTILATE_CAMERA
    key = ACTIONS_NAMES.VENTILATE_CAMERA

    # args_info = [IntKeyArgument, IntKeyArgument]

    def do_action(self):
        # 1) Ток через фольгу постепенно уменьшается до 0
        ramp = self.sub_action(RampAction)
        ramp.action(0.0, 30)

        # 2) на все ррг команда на ноль
        rrg_close = self.sub_action(SetRrgSccmValueAction)
        for gas in settings.VALVES_CONFIGURATION:
            rrg_close.action(gas["NAME"], 0.0)

        # 3) закрываются все клапаны
        close_valves = self.sub_action(CloseAllValvesAction)
        close_valves.action()

        # 4) на клапан обратного давления команда полностью закрыть
        close_throttle = self.sub_action(FullCloseThrottleAction)
        close_throttle.action()

        # 5) ожидаем 30 секунд пока всё точно остынет
        pause = self.sub_action(PauseAction)
        pause.action(30)

        # 6) включается ррг аргона
        ar_name = "Ar"
        ar_sccm = 200.0  # list(filter(lambda x: x["NAME"] == ar_name, settings.VALVES_CONFIGURATION))[0]['']

        ar_rrg = self.sub_action(SetRrgSccmValueAction)
        ar_rrg.action(ar_name, ar_sccm)

        # 7) открываем клапан аргона
        valve_open = self.sub_action(OpenValveAction)
        valve_open.action(ar_name)

        # 8) ожидаем пока давление не станет 950 мбар
        stabilize_pressure = self.sub_action(StabilizePressureAction)
        stabilize_pressure.action(950.0, 1.0, 1)

        # 9) ожидаем 30 сек
        pause.action(30)

        # 10) на ррг аргона команда на ноль
        ar_rrg.action(ar_name, 0.0)

        # 11) закрываем клапан аргона
        valve_close = self.sub_action(CloseValveAction)
        valve_close.action(ar_name)


class RampAction(AppAction):
    name = TABLE_ACTIONS_NAMES.RAMP
    key = ACTIONS_NAMES.RAMP
    args_info = [FloatKeyArgument, TimeEditArgument]

    def do_action(self, target_current: float, seconds: int):

        self.system.target_current_ramp_effect(target_current)

        self.system.is_active_ramp_effect(True)

        pause = 1  # secs
        seconds = max(pause, seconds)

        end_time = self.start_time + seconds
        left_time = end_time - time.time()

        current_value = self.system.current_value
        start_current_value = current_value
        # local_current_value = current_value
        total_current_delta = target_current - current_value

        # # delta_value = target_current - current_value

        def get_next_target():
            if left_time < pause * 0.5:
                return target_current
            time_coef = (time.time() - self.start_time) / seconds
            return total_current_delta * time_coef + start_current_value
            # delta_value = target_current - local_current_value
            # return delta_value / left_time * pause + local_current_value

        while True:
            if self._is_stop_state():
                break

            left_time = max(0.0, end_time - time.time())
            next_target_current = get_next_target()
            # print("NEXT TARGET:", next_target_current)
            self.system.target_current_effect(next_target_current)
            self.system.ramp_seconds_effect(left_time)

            if left_time <= 0:
                break

            time.sleep(1)

            current_value = self.system.current_value
            # local_current_value = current_value

            delta_time = time.time() - self.start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                raise NotAchievingActionGoal

        # time.sleep(4)
        self.system.is_active_ramp_effect(False)


class SetTargetTemperatureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_TARGET_TEMPERATURE
    key = ACTIONS_NAMES.SET_TARGET_TEMPERATURE
    args_info = [IntKeyArgument]

    def do_action(self, target_temperature: int):
        self.system.target_temperature_effect(target_temperature)


class TemperatureRegulationAction(AppAction):
    """
    Not for table recipe using: use with background action wrapper
    """
    name = TABLE_ACTIONS_NAMES.TEMPERATURE_REGULATION
    key = ACTIONS_NAMES.TEMPERATURE_REGULATION
    args_info = []

    last_error = 0.0
    integral = 0.0
    old_speed = 10.0

    def do_action(self):
        # target_temperature = self.system.target_temperature
        self.old_speed = self.system.pid_speed

        # Define PID constants
        Kp = 0.01
        Ki = 0.00001 * self.old_speed  # 0.001 / 10 * speed
        Kd = 0.0

        pause = 0.3

        # Define initial values
        self.last_error = 0.0
        self.integral = 0.0
        self.prev_temperature = 0.0

        self.start_current = self.system.current_value
        print("start pid current:", self.start_current)

        # Define function to calculate PID output
        def calculate_pid_output():
            if abs(self.old_speed - self.system.pid_speed) >= 0.01 and \
                    self.system.pid_speed > 0.0:
                correct_integral_coef = self.old_speed / self.system.pid_speed
                self.old_speed = self.system.pid_speed
                self.integral *= correct_integral_coef

            current_temperature = self.system.pyrometer_temperature_value
            error = self.system.target_temperature - current_temperature

            self.integral += error
            derivative = error - self.last_error
            self.last_error = error

            output = Kp * error + Ki * self.old_speed * self.integral + Kd * derivative

            # print("PID additional current: ", output)
            # print("PID set current: ", self.start_current + output)

            self.prev_temperature = current_temperature

            return self.start_current + output

        while True:
            self.interrupt_if_stop_state()

            # Calculate PID output
            new_current = calculate_pid_output()
            self.system.target_current_effect(new_current)

            # Set current through current source
            # print("Current: ", set_current(pid_output), " A", "actual temp: ", current_temperature, " C")

            time.sleep(pause)


class StartTemperatureRegulationAction(AppAction):
    name = TABLE_ACTIONS_NAMES.START_TEMPERATURE_REGULATION
    key = ACTIONS_NAMES.START_TEMPERATURE_REGULATION

    def do_action(self):
        self.system.is_temperature_regulation_active_effect(True)


class StopTemperatureRegulationAction(AppAction):
    name = TABLE_ACTIONS_NAMES.STOP_TEMPERATURE_REGULATION
    key = ACTIONS_NAMES.STOP_TEMPERATURE_REGULATION

    def do_action(self):
        self.system.is_temperature_regulation_active_effect(False)


class StabilizePressureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.STABILIZE_PRESSURE
    key = ACTIONS_NAMES.STABILIZE_PRESSURE
    args_info = [FloatArgument, FloatKeyArgument, TimeEditArgument]

    def do_action(self, target_pressure: float, error_rate: float, stabilize_seconds: int):

        error_rate = max(0.0, min(100.0, error_rate)) / 100.0
        borders = [
            target_pressure * (1.0 - error_rate),
            target_pressure * (1.0 + error_rate),
        ]

        while True:
            self.interrupt_if_stop_state()

            time.sleep(0.5)
            current_pressure = self.system.accurate_vakumetr_value

            if MAX_RECIPE_STEP_SECONDS and (time.time() - self.start_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Стабилизация давления не завершилась до достижения максимального времени")
                raise NotAchievingActionGoal

            start_stabilization_time = time.time()
            success = False
            while borders[0] <= current_pressure <= borders[1]:
                current_pressure = self.system.accurate_vakumetr_value
                if time.time() - start_stabilization_time >= stabilize_seconds:
                    success = True
                    break

                if MAX_RECIPE_STEP_SECONDS and (time.time() - self.start_time >= MAX_RECIPE_STEP_SECONDS):
                    self.system.add_error_log(f"Стабилизация давления не завершилась до достижения максимального времени")
                    raise NotAchievingActionGoal

            if success:
                break


class WaitRaisePressureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.RAISE_PRESSURE
    key = ACTIONS_NAMES.RAISE_PRESSURE
    args_info = [FloatArgument, FloatKeyArgument, TimeEditArgument]

    def do_action(self, target_pressure_raise: float, error_rate: float, stabilize_seconds: int):
        target_pressure = self.system.accurate_vakumetr_value + target_pressure_raise

        error_rate = max(0.0, min(100.0, error_rate)) / 100.0
        borders = [
            target_pressure * (1.0 - error_rate),
            target_pressure * (1.0 + error_rate),
        ]

        while True:
            self.interrupt_if_stop_state()

            time.sleep(0.5)
            current_pressure = self.system.accurate_vakumetr_value

            if MAX_RECIPE_STEP_SECONDS and (time.time() - self.start_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Стабилизация давления не завершилась до достижения максимального времени")
                raise NotAchievingActionGoal

            start_stabilization_time = time.time()
            success = False
            while borders[0] <= current_pressure <= borders[1]:
                current_pressure = self.system.accurate_vakumetr_value
                if time.time() - start_stabilization_time >= stabilize_seconds:
                    success = True
                    break

                if MAX_RECIPE_STEP_SECONDS and (time.time() - self.start_time >= MAX_RECIPE_STEP_SECONDS):
                    self.system.add_error_log(f"Стабилизация давления не завершилась до достижения максимального времени")
                    raise NotAchievingActionGoal

            if success:
                break


class StabilizeTemperatureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.STABILIZE_TEMPERATURE
    key = ACTIONS_NAMES.STABILIZE_TEMPERATURE
    args_info = [IntKeyArgument, FloatKeyArgument, TimeEditArgument]

    def do_action(self, target_temperature: float, error_rate: float, stabilize_seconds: int):

        error_rate = max(0.0, min(100.0, error_rate)) / 100.0
        borders = [
            target_temperature * (1.0 - error_rate),
            target_temperature * (1.0 + error_rate),
        ]

        while True:
            self.interrupt_if_stop_state()

            time.sleep(0.5)
            current_temperature = self.system.pyrometer_temperature_value

            if MAX_RECIPE_STEP_SECONDS and (time.time() - self.start_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Стабилизация давления не завершилась до достижения максимального времени")
                raise NotAchievingActionGoal

            start_stabilization_time = time.time()
            success = False
            while borders[0] <= current_temperature <= borders[1]:
                current_temperature = self.system.pyrometer_temperature_value
                if time.time() - start_stabilization_time >= stabilize_seconds:
                    success = True
                    break

                if MAX_RECIPE_STEP_SECONDS and (time.time() - self.start_time >= MAX_RECIPE_STEP_SECONDS):
                    self.system.add_error_log(f"Стабилизация давления не завершилась до достижения максимального времени")
                    raise NotAchievingActionGoal

            if success:
                break


ACTIONS = [
    TurnOnPumpAction(),
    TurnOffPumpAction(),
    OpenValveAction(),
    CloseValveAction(),
    CloseAllValvesAction(),
    SetRrgSccmValueAction(),
    SetRrgSccmValueWithPauseAction(),
    PumpOutCameraAction(),
    VentilateCameraAction(),

    SetThrottlePressureAction(),
    FullOpenThrottleAction(),
    FullCloseThrottleAction(),
    SetThrottlePercentAction(),

    SetTargetTemperatureAction(),
    StartTemperatureRegulationAction(),
    StopTemperatureRegulationAction(),

    PauseAction(),
    StabilizePressureAction(),
    StabilizeTemperatureAction(),
    WaitRaisePressureAction(),

    RampAction(),
]

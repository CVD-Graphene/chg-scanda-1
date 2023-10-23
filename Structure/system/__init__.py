import gc
import random
import time
from threading import Thread, get_ident

from Core.actions import PidTemperatureBackgroundAction
from Core.actions.actions import RampAction, PumpOutCameraAction, VentilateCameraAction
from coregraphene.actions import BaseThreadAction
from coregraphene.system_effects import SingleAnswerSystemEffect
from .effects import (
    ChangeGasValveStateEffect,
    ChangeAirValveStateEffect,
    SetTargetCurrentEffect,
    SetRampSecondsEffect,
    SetTargetCurrentRampEffect,
    SetIsRampActiveEffect,
    SetIsRampWaitingEffect,
    SetTargetRrgSccmEffect,
    FullCloseRrgEffect,
    FullOpenRrgEffect,
    ChangePumpValveStateEffect,
    ChangePumpManageStateEffect,
    SetTargetTemperatureSystemEffect,
    SetIsTemperatureRegulationActiveEffect,
    SetTemperaturePidSpeedSystemEffect, ChangeTmpPumpStateEffect,
)
from coregraphene.components.controllers import (
    AbstractController,
    AccurateVakumetrController,
    ValveController,
    CurrentSourceController,
    PyrometerTemperatureController,
    SeveralRrgAdcDacController,
    DigitalFuseController,
    BackPressureValveController,
    VakumetrAdcController, BhRrgController, SeveralRrgModbusController, RrgModbusController, BhVakumetrController,
    TetronCurrentSourceController,
)
from coregraphene.system import BaseSystem
from coregraphene.conf import settings
from coregraphene.utils import get_available_ttyusb_ports, get_available_ttyusb_port_by_usb

VALVES_CONFIGURATION = settings.VALVES_CONFIGURATION
LOCAL_MODE = settings.LOCAL_MODE


class AppSystem(BaseSystem):
    current_value = 0.0
    voltage_value = 0.0
    target_current_value = 0.0
    target_current_ramp_value = 0.0
    ramp_seconds = 0
    ramp_active = False
    ramp_waiting = False

    target_temperature = 0
    pid_speed = 10.0
    temperature_regulation = False

    _default_controllers_kwargs = {
        'vakumetr': {
            'port_communicator': settings.ACCURATE_VAKUMETR_COMMUNICATOR_PORT,
            'baudrate': settings.ACCURATE_VAKUMETR_BAUDRATE,
        },
        'current_source': {
            # 'port_communicator': settings.CURRENT_SOURCE_COMMUNICATOR_PORT,
            'baudrate': settings.CURRENT_SOURCE_BAUDRATE,
            'timeout': settings.CURRENT_SOURCE_TIMEOUT,
        },
        'pyrometer': {
            'baudrate': settings.PYROMETER_TEMPERATURE_BAUDRATE,
        },
        'bh_rrg': {
            'baudrate': settings.BH_RRG_CONTROLLER_BAUDRATE,
            'port': settings.BH_RRG_CONTROLLER_USB_PORT,
            'rrg_config': VALVES_CONFIGURATION,
            'timeout': 0.3,
            'create_instrument_delay': 3,
            'max_rrg_voltage': settings.BH_RRG_CONTROLLER_MAX_RRG_VOLTAGE,
            # 'immediate_serial_read': True,
        },
    }

    _ports_attr_names = {
        'vakumetr': 'vakumetr_port',
        'rrg': 'rrg_port',
        'current_source': 'current_source_port',
        'pyrometer': 'pyrometer_temperature_port',
        # 'throttle': 'back_pressure_valve_port',
    }

    _usb_devices_ports = {
        'vakumetr': settings.ACCURATE_VAKUMETR_USB_PORT,
        'rrg': settings.RRG_USB_PORT,
        'current_source': settings.CURRENT_SOURCE_USB_PORT,
        'pyrometer': settings.PYROMETER_TEMPERATURE_USB_PORT,
        # 'throttle': settings.BACK_PRESSURE_VALVE_USB_PORT,
    }

    def _determine_attributes(self):
        used_ports = []
        self.vakumetr_port = None
        self.rrg_port = None
        self.current_source_port = None
        self.pyrometer_temperature_port = None
        self.back_pressure_valve_port = None

        # return
        self._controllers_check_classes = {
            # 'throttle': BackPressureValveController,
            'rrg': RrgModbusController,
            'vakumetr': AccurateVakumetrController,
            'pyrometer': PyrometerTemperatureController,
            'current_source': TetronCurrentSourceController,
        }

        for controller_code, port_name_attr in self._ports_attr_names.items():
            if LOCAL_MODE:
                ttyusb_port = '/dev/ttyUSB0'
            else:
                ttyusb_port = get_available_ttyusb_port_by_usb(
                    self._usb_devices_ports.get(controller_code, '')
                )
            setattr(self, self._ports_attr_names[controller_code], ttyusb_port)

        print(
            "|> FOUND PORTS:",
            "vakumetr:", self.vakumetr_port,
            "rrg:", self.rrg_port,
            'current_source:', self.current_source_port,
            "pyrometer", self.pyrometer_temperature_port,
            # 'throttle', self.back_pressure_valve_port,
        )
        assert self.vakumetr_port is not None
        assert self.rrg_port is not None
        assert self.current_source_port is not None
        assert self.pyrometer_temperature_port is not None
        # assert self.back_pressure_valve_port is not None

        self.ports = {
            'vakumetr': self.vakumetr_port,
            'rrg': self.rrg_port,
            'current_source': self.current_source_port,
            'pyrometer': self.pyrometer_temperature_port,
            # 'throttle': self.back_pressure_valve_port,
        }

        gc.collect()

    def _init_controllers(self):
        self.accurate_vakumetr_controller = AccurateVakumetrController(
            get_potential_port=self.get_potential_controller_port_1,
            port=self.vakumetr_port,
            **self._default_controllers_kwargs.get('vakumetr'),
        )
        # self.accurate_vakumetr_controller = BhVakumetrController(
        #     # port=self.vakumetr_port,
        #     **self._default_controllers_kwargs.get('bh_rrg'),
        #     get_potential_port=self.get_potential_controller_port_1,
        # )
        self.pyrometer_temperature_controller = PyrometerTemperatureController(
            get_potential_port=self.get_potential_controller_port_1,
            port=self.pyrometer_temperature_port,
            **self._default_controllers_kwargs.get('pyrometer'),
        )

        self.air_valve_controller = ValveController(
            port=settings.AIR_VALVE_CONFIGURATION['PORT'],
        )

        # self.bh_rrg_controller = BhRrgController(
        #     get_potential_port=self.get_potential_controller_port_1,
        #     **self._default_controllers_kwargs.get('bh_rrg'),
        # )
        self.rrgs_controller = SeveralRrgModbusController(
            config=VALVES_CONFIGURATION,
            get_potential_port=self.get_potential_controller_port_1,
            port=self.rrg_port,
        )

        # PUMP BLOCK
        self.pump_valve_controller = ValveController(
            port=settings.PUMP_CONFIGURATION['VALVE_PORT'],
        )
        self.pump_manage_controller = ValveController(
            port=settings.PUMP_CONFIGURATION['MANAGE_PORT'],
        )
        # self.back_pressure_valve_controller = BackPressureValveController(
        #     get_potential_port=self.get_potential_controller_port_1,
        #     port=self.back_pressure_valve_port,
        #     **self._default_controllers_kwargs.get('throttle'),
        # )
        self.small_tmp_pump = ValveController(port=12)
        ##############

        self._valves = {}
        # for valve_conf in VALVES_CONFIGURATION:
        #     self._valves[valve_conf["NAME"]] = ValveController(port=valve_conf["PORT"])
        for i, valve_conf in enumerate(VALVES_CONFIGURATION):
            self._valves[i] = ValveController(port=valve_conf["PORT"])

        # self.rrgs_controller = SeveralRrgAdcDacController(
        #     config=VALVES_CONFIGURATION,
        #     read_channel=settings.RRG_SPI_READ_CHANNEL,
        #     write_channel=settings.RRG_SPI_WRITE_CHANNEL,
        #     speed=settings.RRG_SPI_SPEED,
        #     read_device=settings.RRG_SPI_READ_DEVICE,
        #     write_device=settings.RRG_SPI_WRITE_DEVICE,
        # )

        # self.gases_pressure_controller = VakumetrAdcController(
        #     config=VALVES_CONFIGURATION,
        #     channel=settings.VAKUMETR_SPI_READ_CHANNEL,
        #     speed=settings.VAKUMETR_SPI_SPEED,
        #     device=settings.VAKUMETR_SPI_READ_DEVICE,
        # )

        self._digital_fuses = {}
        for i, port in enumerate(settings.DIGITAL_FUSE_PORTS):
            self._digital_fuses[i] = DigitalFuseController(port=port)

        self.current_source_controller = TetronCurrentSourceController(
            port=self.current_source_port,
            **self._default_controllers_kwargs.get('current_source'),
        )

        self._controllers: list[AbstractController] = [
            self.accurate_vakumetr_controller,
            self.air_valve_controller,
            self.pyrometer_temperature_controller,
            self.rrgs_controller,
            self.small_tmp_pump,
            # self.bh_rrg_controller,
            # self.gases_pressure_controller,
            self.current_source_controller,

            self.pump_valve_controller,
            self.pump_manage_controller,
            # self.back_pressure_valve_controller,
        ]

        for valve in self._valves.values():
            self._controllers.append(valve)

        for fuse in self._digital_fuses.values():
            self._controllers.append(fuse)

    def _init_actions(self):
        super()._init_actions()

        # ===== TMP PUMP ======== #
        self.change_tmp_pump_opened = ChangeTmpPumpStateEffect(system=self)

        # ===== Valves ======== #
        self.change_gas_valve_opened = ChangeGasValveStateEffect(system=self)
        self.change_air_valve_opened = ChangeAirValveStateEffect(system=self)

        # ===== PUMP ========== #
        self.change_pump_valve_opened_effect = ChangePumpValveStateEffect(system=self)
        self.change_pump_manage_active_effect = ChangePumpManageStateEffect(system=self)

        # ===== RRG =========== #
        self.set_target_rrg_sccm_effect = SetTargetRrgSccmEffect(system=self)
        self.full_close_rrg_effect = FullCloseRrgEffect(system=self)
        self.full_open_rrg_effect = FullOpenRrgEffect(system=self)

        self.current_rrg_sccm_effect = SingleAnswerSystemEffect(system=self)
        self.rrgs_controller.get_current_flow.connect(self.current_rrg_sccm_effect)
        # self.bh_rrg_controller.get_current_flow.connect(self.current_rrg_sccm_effect)

        # ===== Vakumetr gases ==== #
        self.current_gas_balloon_pressure_effect = SingleAnswerSystemEffect(system=self)
        # self.gases_pressure_controller.get_current_pressure_action.connect(
        #     self.current_gas_balloon_pressure_effect)

        # ===== Pyrometer ===== #
        self.current_temperature_effect = SingleAnswerSystemEffect(system=self)
        self.current_temperature_effect.connect(self._on_get_current_temperature)
        self.pyrometer_temperature_controller.get_temperature_action \
            .connect(self.current_temperature_effect)

        # ===== Temperature regulation ===== #
        self.target_temperature_effect = SetTargetTemperatureSystemEffect(system=self)
        self.is_temperature_regulation_active_effect = SetIsTemperatureRegulationActiveEffect(system=self)
        self.temperature_pid_speed_effect = SetTemperaturePidSpeedSystemEffect(system=self)

        # ===== Current AKIP ========= #
        self.target_current_effect = SetTargetCurrentEffect(system=self)

        self.actual_current_effect = SingleAnswerSystemEffect(system=self)
        self.actual_current_effect.connect(self._on_get_actual_current)
        self.current_source_controller.actual_current_effect.connect(self.actual_current_effect)

        self.actual_voltage_effect = SingleAnswerSystemEffect(system=self)
        self.actual_voltage_effect.connect(self._on_get_actual_voltage)
        self.current_source_controller.actual_voltage_effect.connect(self.actual_voltage_effect)

        self.is_power_current_source_effect = SingleAnswerSystemEffect(system=self)
        self.current_source_controller.is_power_effect.connect(self.is_power_current_source_effect)

        self.ramp_seconds_effect = SetRampSecondsEffect(system=self)
        self.target_current_ramp_effect = SetTargetCurrentRampEffect(system=self)

        self.is_active_ramp_effect = SetIsRampActiveEffect(system=self)
        self.is_waiting_ramp_effect = SetIsRampWaitingEffect(system=self)

        # ===== Throttle: back pressure valve == #
        # self.throttle_state_effect = SingleAnswerSystemEffect(system=self)
        # self.back_pressure_valve_controller.get_state_action.connect(self.throttle_state_effect)
        #
        # self.throttle_current_pressure_effect = SingleAnswerSystemEffect(system=self)
        # self.back_pressure_valve_controller.get_current_pressure_action. \
        #     connect(self.throttle_current_pressure_effect)
        #
        # self.throttle_target_pressure_effect = SingleAnswerSystemEffect(system=self)
        # self.back_pressure_valve_controller.get_target_pressure_action. \
        #     connect(self.throttle_target_pressure_effect)
        #
        # self.throttle_target_open_percent_effect = SingleAnswerSystemEffect(system=self)
        # self.back_pressure_valve_controller.get_target_open_percent_action. \
        #     connect(self.throttle_target_open_percent_effect)

        # ===== Accurate vakumetr ===== #
        self.accurate_vakumetr_effect = SingleAnswerSystemEffect(system=self)
        self.accurate_vakumetr_controller.actual_pressure_effect. \
            connect(self.accurate_vakumetr_effect)
        self.accurate_vakumetr_effect.connect(self._on_get_accurate_vakumetr_value)
        # self.accurate_vakumetr_controller.get_current_pressure_effect. \
        #     connect(self.accurate_vakumetr_effect)

        #########################

    def _init_values(self):
        self.accurate_vakumetr_value = 0.0
        self.pyrometer_temperature_value = 0.0
        self.target_temperature = 0
        self.pid_speed = 10.0
        # self.current_value = 0.0
        # self.voltage_value = 0.0

    def create_background_actions_array(self):
        pid_temperature_background_action = PidTemperatureBackgroundAction(system=self)
        pid_temperature_background_action.is_stop_state_function = \
            self._pid_temperature_is_stop_function

        return [
            pid_temperature_background_action,
        ]

    def _pid_temperature_is_stop_function(self):
        return not (self.is_working() and self.temperature_regulation)

    def pause_test(self):
        secs = random.random() * 20 + 5
        time.sleep(secs)
        print("I SLEEP", secs, "ident:", get_ident())

    def test_ramp(self):
        arr = []
        for _ in range(30):
            th = Thread(target=self.pause_test)
            th.start()
            # th.is_alive()
            # time.sleep(1)
            arr.append(th)
        # pops = []
        while arr:
            for i, thread in enumerate(arr):
                if not thread.is_alive():
                    thread.join()
                    print('TH NAME JOINED:', thread.getName())
                    arr.pop(i)
                    break
            time.sleep(0.2)
        print("ENDING!")

    def on_ramp_press_start(self, *args):
        try:
            if self.ramp_waiting:
                return
            self.is_waiting_ramp_effect(True)
            if self.ramp_active:
                self.ramp_active = False
                return

            thread_action = BaseThreadAction(
                system=self,
                action=RampAction,
            )
            thread_action.set_action_args(
                self.target_current_ramp_value,
                self.ramp_seconds,
            )
            thread_action.action.is_stop_state_function = self._ramp_is_stop_function
            self._add_action_to_loop(thread_action=thread_action)

        except Exception as e:
            print("ERR RAMP START:", e)

    def _ramp_is_stop_function(self):
        return not (self.is_working() and self.ramp_active)

    def on_temperature_regulation_press(self):
        try:
            self.is_temperature_regulation_active_effect(not self.temperature_regulation)
        except Exception as e:
            print("ERR PID START:", e)

    def on_pump_press(self):
        try:
            recipe = [[PumpOutCameraAction.name]]
            self.set_recipe(recipe)
            ready = self.check_recipe_is_correct()
            if not ready:
                return
            self.run_recipe()
        except Exception as e:
            self.add_error("Start recipe PUMP:" + str(e))
            print("Start recipe UI PUMP error:", e)

    def on_vent_press(self):
        try:
            recipe = [[VentilateCameraAction.name]]
            self.set_recipe(recipe)
            ready = self.check_recipe_is_correct()
            if not ready:
                return
            self.run_recipe()
        except Exception as e:
            self.add_error("Start recipe VENT:" + str(e))
            print("Start recipe UI VENT error:", e)

    def check_conditions(self):
        return True

    def log_state(self):
        pass

    def _change_valve_state(self, valve, name="-"):
        new_state = valve.change_state()
        # print(f"Valve {name} new state: {new_state}")
        return new_state

    @BaseSystem.action
    def change_valve_state(self, gas_num):
        valve = self._valves.get(gas_num, None)
        if valve is None:
            return False
        new_state = self._change_valve_state(valve, gas_num)
        self.change_gas_valve_opened(new_state, device_num=gas_num)

    @BaseSystem.action
    def change_tmp_pump_state(self):
        new_state = self.small_tmp_pump.change_state()
        self.change_tmp_pump_opened(new_state)

    @BaseSystem.action
    def change_air_valve_state(self):
        new_state = self._change_valve_state(self.air_valve_controller, "AIR")
        self.change_air_valve_opened(new_state)

    @BaseSystem.action
    def change_pump_valve_state(self):
        new_state = self._change_valve_state(self.pump_valve_controller, "PUMP V")
        self.change_pump_valve_opened_effect(new_state)

    @BaseSystem.action
    def change_pump_manage_state(self):
        new_state = self._change_valve_state(self.pump_manage_controller, "PUMP M")
        self.change_pump_manage_active_effect(new_state)

    @BaseSystem.action
    def set_target_current(self, value):
        return self.current_source_controller.set_target_current(value)

    def _on_get_current_temperature(self, value):
        self.pyrometer_temperature_value = value

    def _on_get_actual_current(self, value):
        self.current_value = value

    def _on_get_actual_voltage(self, value):
        self.voltage_value = value

    def _on_get_accurate_vakumetr_value(self, value):
        self.accurate_vakumetr_value = value

    def get_accurate_vakumetr_value(self):
        return self.accurate_vakumetr_value

    def set_ramp_seconds(self, value):
        try:
            self.ramp_seconds = int(value)
        except:
            self.ramp_seconds = 0
        return self.ramp_seconds

    def set_target_current_ramp_value(self, value):
        try:
            self.target_current_ramp_value = float(value)
        except:
            self.target_current_ramp_value = 0.0
        return self.target_current_ramp_value

    def set_is_ramp_active(self, value):
        self.ramp_active = bool(value)
        self.is_waiting_ramp_effect(False)
        return self.ramp_active

    def set_is_ramp_waiting(self, value):
        self.ramp_waiting = bool(value)
        return self.ramp_waiting

    def set_target_temperature_value(self, value):
        # print("SET TARGET [set_target_temperature_value]:", value)
        try:
            self.target_temperature = int(value)
        except:
            self.target_temperature = 0
        return self.target_temperature

    def set_temperature_pid_speed_value(self, value: float):
        # print("SET TARGET [set_target_temperature_value]:", value)
        try:
            value = min(10000.0, max(0.01, float(value)))
            self.pid_speed = value
        except:
            self.pid_speed = 10.0
        return self.pid_speed

    # def set_is_temperature_regulation_active(self, value):
    #     self.temperature_regulation = bool(value)
    #     return self.temperature_regulation

    def _get_values(self):
        pass

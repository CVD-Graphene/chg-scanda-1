from coregraphene.conf import settings
from coregraphene.exceptions import BaseConditionException
from coregraphene.system_effects import ManyDeviceSystemEffect, SystemEffect

LOCAL_MODE = settings.LOCAL_MODE


class ChangeAirValveStateEffect(SystemEffect):
    def _call_function(self, is_open):
        if is_open:
            # 1 - проверка что НЕ открыт клапан на турбомолекулярный насос
            if self._system.tc110_valve.is_open:
                raise BaseConditionException(
                    f"Нельзя открыть, если клапан турбомолекулярного насоса открыт")

        return self._system.air_valve_controller.set_is_open_state(is_open)


class ChangeGasValveStateEffect(ManyDeviceSystemEffect):
    def _call_function(self, is_open, device_num=None):
        if is_open:
            # 1 - проверка что НЕ открыт клапан на турбомолекулярный насос
            if self._system.tc110_valve.is_open:
                raise BaseConditionException(
                    f"Нельзя открыть, если клапан турбомолекулярного насоса открыт")

        return self._system._valves[device_num].set_is_open_state(is_open)


class ChangeTmpPumpStateEffect(ManyDeviceSystemEffect):
    def _call_function(self, is_open):
        if is_open:
            # 1 - проверка что НЕ открыт клапан на турбомолекулярный насос
            if self._system.tc110_valve.is_open:
                raise BaseConditionException(
                    f"Нельзя открыть, если клапан турбомолекулярного насоса открыт")

        return self._system.small_tmp_pump.set_is_open_state(is_open)


class ChangeTc110FuseStateEffect(ManyDeviceSystemEffect):
    def _call_function(self, is_open):
        if is_open:
            # 1 - проверка что НЕ открыт ЛЮБОЙ ДРУГОЙ клапан
            s = self._system
            gas_open = False
            for valve in s._valves.values():
                if valve.is_open:
                    gas_open = True
                    break

            if (
                    gas_open
                    or s.small_tmp_pump.is_open
                    or s.air_valve_controller.is_open
                    or s.pump_valve_controller.is_open
            ):
                raise BaseConditionException(
                    f"Нельзя открывать клапан на турбомолекулярный насос одновременно с любым другим клапаном")
            # 2
            if self._system.accurate_vakumetr_value >= settings.TURBO_MOLECULAR_PUMP_CRITICAL_PRESSURE:
                raise BaseConditionException(
                    f"Нельзя включить при большом давлении в камере: {self._system.accurate_vakumetr_value}")

        return self._system.tc110_valve.set_is_open_state(is_open)


# =========== PUMP
class ChangePumpValveStateEffect(SystemEffect):
    def _call_function(self, is_open):  # tc110_valve
        if is_open:
            # 1 - проверка что НЕ открыт клапан на турбомолекулярный насос
            if self._system.tc110_valve.is_open:
                raise BaseConditionException(
                    f"Нельзя открыть, если клапан турбомолекулярного насоса открыт")

        return self._system.pump_valve_controller.set_is_open_state(is_open)


class ChangePumpManageStateEffect(SystemEffect):
    def _call_function(self, is_open):
        if not is_open:
            # 1 - проверка что НЕ работает турбомолекулярный насос
            if self._system.pump_tc110_controller.is_working:
                raise BaseConditionException(
                    f"Нельзя выключить, если турбомолекулярный насос работает")

        return self._system.pump_manage_controller.set_is_open_state(is_open)


class ChangePumpTC110ManageStateEffect(SystemEffect):
    def _call_function(self, is_on):
        if is_on:  # хотим включить турбик
            # 1 - проверка что работает форвакуумный насос
            if not self._system.pump_manage_controller.is_open:
                raise BaseConditionException(
                    f"Нельзя включить, если форвакуумный насос выключен")
                return False

            # 2 - если давление в камере очень большое, то запрет операции
            if self._system.accurate_vakumetr_value < settings.TURBO_MOLECULAR_PUMP_CRITICAL_PRESSURE:
                return self._system.pump_tc110_controller.pump_turn_on()
            else:
                raise BaseConditionException(
                    f"Нельзя включить при большом давлении в камере: {self._system.accurate_vakumetr_value}")
                return False
        else:
            return self._system.pump_tc110_controller.pump_turn_off()


class SetAccurateVakumetrValueEffect(SystemEffect):
    def _call_function(self, value, **kwargs):  # Here with device_num :(
        # print(kwargs)
        self._system.accurate_vakumetr_value = value
        # если давление в камере большое, то проверяем на состояние тубрик и клапан
        if self._system.accurate_vakumetr_value >= settings.TURBO_MOLECULAR_PUMP_CRITICAL_PRESSURE and (True or not LOCAL_MODE):
            bad_config = False
            if self._system.tc110_valve.is_open:
                self._system.change_tc110_fuse_opened(False)
                bad_config = True
                # self._system.add_error(Exception(f"ЭКСТРЕННАЯ ОСТАНОВКА ТУРБОМОЛЕКУЛЯРНОГО НАСОСА"))

            if self._system.pump_tc110_controller.is_active:
                self._system.change_pump_tc110_active_effect(False)
                bad_config = True

            if bad_config:
                raise BaseConditionException("ЭКСТРЕННАЯ ОСТАНОВКА ТУРБОМОЛЕКУЛЯРНОГО НАСОСА")
                # self._system.add_error(Exception(f"ЭКСТРЕННАЯ ОСТАНОВКА ТУРБОМОЛЕКУЛЯРНОГО НАСОСА"))

        return self._system._on_get_accurate_vakumetr_value(value)


# ======== PUMP TC110
class SetTargetSpeedPumpTC110SystemEffect(SystemEffect):
    def _call_function(self, value):
        print(f'|> New PUMP-TC110 target speed: {value}')
        return self._system.pump_tc110_controller.set_target_speed_percent(value)


# ======== RRG
class SetTargetRrgSccmEffect(ManyDeviceSystemEffect):
    def _call_function(self, sccm, device_num):
        print('{{{ SetTargetRrgSccmEffect }}}', sccm, device_num)
        return self._system.rrgs_controller.set_target_sccm(sccm, device_num)


class FullCloseRrgEffect(ManyDeviceSystemEffect):
    def _call_function(self, device_num):
        # print('{{{ FullCloseRrgEffect', device_num)
        return self._system.rrgs_controller.full_rrg_close(device_num)


class FullOpenRrgEffect(ManyDeviceSystemEffect):
    def _call_function(self, device_num):
        # print('{{{ FullOpenRrgEffect', device_num)
        return self._system.rrgs_controller.full_rrg_open(device_num)


class SetTargetCurrentEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_target_current(value)


class SetRampSecondsEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_ramp_seconds(int(value))


class SetTargetCurrentRampEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_target_current_ramp_value(value)


class SetIsRampActiveEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_is_ramp_active(value)


class SetIsRampWaitingEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_is_ramp_waiting(value)


# TEMPERATURE


class SetTargetTemperatureSystemEffect(SystemEffect):
    def _call_function(self, value):
        print(f'|> New PID target temperature: {value}')
        return self._system.set_target_temperature_value(value)


class SetTemperaturePidSpeedSystemEffect(SystemEffect):
    def _call_function(self, value):
        print(f'|> New PID speed: {value}')
        return self._system.set_temperature_pid_speed_value(value)


class SetIsTemperatureRegulationActiveEffect(SystemEffect):
    def _call_function(self, value):
        return value
        # return self._system.set_is_ramp_active(value)

    def _on_get_value(self, value):
        self._system.temperature_regulation = bool(value)

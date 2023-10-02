class ACTIONS_NAMES:
    RAMP = "RAMP"
    TURN_ON_PUMP = "TURN_ON_PUMP"
    TURN_OFF_PUMP = "TURN_OFF_PUMP"

    OPEN_VALVE = "OPEN_VALVE"
    CLOSE_VALVE = "CLOSE_VALVE"
    CLOSE_ALL_VALVES = "CLOSE_ALL_VALVES"

    FULL_OPEN_RRG = "FULL_OPEN_RRG"
    FULL_CLOSE_RRG = "FULL_CLOSE_RRG"
    SET_RRG_VALUE = "SET_RRG_VALUE"
    SET_RRG_VALUE_WITH_PAUSE = "SET_RRG_VALUE_WITH_PAUSE"
    SET_RRG_AND_KEEP_TO_PRESSURE = "SET_RRG_AND_KEEP_TO_PRESSURE"

    PUMP_OUT_CAMERA = "PUMP_OUT_CAMERA"
    VENTILATE_CAMERA = "VENTILATE_CAMERA"
    SMALL_PUMP_OUT_CAMERA = "SMALL_PUMP_OUT_CAMERA"

    TURN_ON_ALL_TERMODATS = "TURN_ON_ALL_TERMODATS"
    TURN_OFF_ALL_TERMODATS = "TURN_OFF_ALL_TERMODATS"
    SET_T_V_ALL_TERMODATS = "SET_T_V_ALL_TERMODATS"
    WAIT_TARGET_TEMPERATURE = "WAIT_TARGET_TEMPERATURE"

    SET_TEMPERATURE = "SET_TEMPERATURE"
    SET_TEMPERATURE_IN_TIME = "SET_TEMPERATURE_IN_TIME"
    SET_TEMPERATURE_FOR_TERMODAT_DEVICE = "SET_TEMPERATURE_FOR_TERMODAT_DEVICE"
    SET_SPEED_FOR_TERMODAT_DEVICE = "SET_SPEED_FOR_TERMODAT_DEVICE"

    PAUSE = "PAUSE"
    QUICK_SHUTDOWN_DEVICE = "QUICK_SHUTDOWN_DEVICE"

    FULL_OPEN_PUMP = "FULL_OPEN_PUMP"
    FULL_CLOSE_PUMP = "FULL_CLOSE_PUMP"
    STABILIZE_PRESSURE = "STABILIZE_PRESSURE"
    STABILIZE_TEMPERATURE = "STABILIZE_TEMPERATURE"
    RAISE_PRESSURE = "RAISE_PRESSURE"

    SET_TARGET_TEMPERATURE = "SET_TARGET_TEMPERATURE"
    SET_THROTTLE_PERCENT = "SET_THROTTLE_PERCENT"
    FULL_OPEN_THROTTLE = "FULL_OPEN_THROTTLE"
    FULL_CLOSE_THROTTLE = "FULL_CLOSE_THROTTLE"
    SET_THROTTLE_PRESSURE = "SET_THROTTLE_PRESSURE"

    TEMPERATURE_REGULATION = "TEMPERATURE_REGULATION"
    START_TEMPERATURE_REGULATION = "START_TEMPERATURE_REGULATION"
    STOP_TEMPERATURE_REGULATION = "STOP_TEMPERATURE_REGULATION"


class TABLE_ACTIONS_NAMES:
    RAMP = "Ramp"
    TURN_ON_PUMP = "Включить насос"
    TURN_OFF_PUMP = "Выключить насос"

    OPEN_VALVE = "Открыть клапан" + " [клапан]"
    CLOSE_VALVE = "Закрыть клапан" + " [клапан]"
    CLOSE_ALL_VALVES = "Закрыть все клапаны"

    SET_RRG_VALUE = "Значение на РРГ" + " [газ, sccm]"
    SET_RRG_VALUE_WITH_PAUSE = "Значение на РРГ с паузой" + " [газ, sccm, мммм:сс]"
    SET_RRG_AND_KEEP_TO_PRESSURE = "Повысить давление газа на определённую величину [газ, sccm, давление]"

    PUMP_OUT_CAMERA = "Откачать камеру"
    VENTILATE_CAMERA = "Провентилировать камеру"
    SMALL_PUMP_OUT_CAMERA = "Откачать камеру игольчатым вентилем" + " [давление, лимит времени]"

    TURN_ON_ALL_TERMODATS = "Включить все печки"
    TURN_OFF_ALL_TERMODATS = "Выключить все печки"
    SET_T_V_ALL_TERMODATS = "Установить T и V на печки" + " [температура, скорость]"
    WAIT_TARGET_TEMPERATURE = "Ждать установления температуры [температура, мммм:сс]"

    PAUSE = "Пауза" + " [время мммм:сс]"
    QUICK_SHUTDOWN_DEVICE = "Полное выключение установки"

    FULL_OPEN_PUMP = "Открыть клапан насоса"
    FULL_CLOSE_PUMP = "Закрыть клапан насоса"
    STABILIZE_PRESSURE = "Стабилизировать давление"
    STABILIZE_TEMPERATURE = "Стабилизировать температуру"
    RAISE_PRESSURE = "Ожидание повышения давления"

    SET_TARGET_TEMPERATURE = "Установить температуру"
    SET_THROTTLE_PERCENT = "Открыть дроссель на X%"
    FULL_OPEN_THROTTLE = "Полностью открыть дроссель"
    FULL_CLOSE_THROTTLE = "Полностью закрыть дроссель"
    SET_THROTTLE_PRESSURE = "Установить давление"

    TEMPERATURE_REGULATION = "Регуляция температуры (НЕ ДЛЯ ТАБЛИЦЫ)"
    START_TEMPERATURE_REGULATION = "Включить регуляцию температуры"
    STOP_TEMPERATURE_REGULATION = "Выключить регуляцию температуры"

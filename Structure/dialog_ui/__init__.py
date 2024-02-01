from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from Core.actions import ACTIONS
from .MainBlockWidget import MainBlockWidget
# from Structure.dialog_ui.RightButtonsWidget import RightButtonsWidget
# from Structure.dialog_ui.TableWidget import AppTableWidget
# from Structure.dialog_ui.components import LogWidget

from coregraphene.conf import settings
from coregraphene.constants import RECIPE_STATES, RECIPE_STATES_TO_STR, NOTIFICATIONS
from grapheneqtui.structures import BaseMainDialogWindow
from .RightButtonsWidget import AppRightButtonsWidget, RecipesButtonsWidget
from ..system import AppSystem


class AppMainDialogWindow(BaseMainDialogWindow):
    main_interface_widget_class = MainBlockWidget
    system: AppSystem = None

    actions_list = ACTIONS
    recipe_states = RECIPE_STATES
    recipe_states_to_str = RECIPE_STATES_TO_STR
    recipe_table_column_names = settings.TABLE_COLUMN_NAMES
    notifications_configuration = NOTIFICATIONS
    right_buttons_block_class = AppRightButtonsWidget

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_right_buttons(self):
        self.recipe_btns = RecipesButtonsWidget(
            parent=self,
            on_open_recipe=self.on_open_recipe,
            on_run_recipe_by_file=self.on_choose_recipe_file,
        )
        self.right_buttons_layout_widget = self.right_buttons_block_class(
            recipe_btns=self.recipe_btns,
            on_close=self.close,
            on_create_recipe=self.on_create_recipe,
            on_open_recipe=self.on_open_recipe,
            on_stop_recipe=self.system.on_stop_recipe,
            on_pause_recipe=self.system.on_pause_recipe,
            on_get_recipe_state=self.system.get_recipe_state,
            recipe_states=self.recipe_states,
        )
        self.main_window.addWidget(self.right_buttons_layout_widget)

    def connect_controllers_actions(self):
        # GASES #################
        for gas in self.milw.pressure_block.gases:
            num = gas.number

            # gas.connect_valve_function(self.system.change_valve_state)
            gas.update_is_valve_open_signal.connect(
                self.system.change_valve_state)
            # self.system.change_gas_valve_opened.connect(
            #     gas.draw_is_open, device_num=num)
            self.system.change_gas_valve_opened.connect(
                gas.on_update_is_valve_open_signal.emit, device_num=num)

            # gas.connect_change_sccm_function(self.system.set_target_rrg_sccm_effect)
            gas.update_target_sccm_signal.connect(self.system.set_target_rrg_sccm_effect)
            self.system.set_target_rrg_sccm_effect.connect(
                gas.column_info.update_target_signal.emit, device_num=gas.number)
            self.system.full_open_rrg_effect.connect(
                gas.column_info.update_target_signal.emit, device_num=gas.number)
            self.system.full_close_rrg_effect.connect(
                gas.column_info.update_target_signal.emit, device_num=gas.number)

            self.system.current_rrg_sccm_effect.connect(
                gas.column_info.update_current_signal.emit, device_num=gas.number)

            # Balloon gas pressure
            self.system.current_gas_balloon_pressure_effect.connect(
                gas.on_update_gas_name_color_by_pressure_signal.emit, device_num=gas.number)

        # AIR #################
        self.milw.pressure_block.air.update_is_valve_open_signal\
            .connect(self.system.change_air_valve_state)
        self.system.change_air_valve_opened.connect(
            self.milw.pressure_block.air.on_update_is_valve_open_signal.emit)
        #######################

        # PUMP ################
        self.milw.pressure_block.pump_block.update_pump_valve_state_signal\
            .connect(self.system.change_pump_valve_state)
        self.system.change_pump_valve_opened_effect.connect(
            self.milw.pressure_block.pump_block.on_update_pump_valve_is_open_signal.emit)

        self.milw.pressure_block.pump_block.update_pump_state_signal\
            .connect(self.system.change_pump_manage_state)
        self.system.change_pump_manage_active_effect.connect(
            self.milw.pressure_block.pump_block.on_update_pump_is_open_signal.emit)

        # << THROTTLE >> #
        self.milw.pressure_block.pump_block.update_throttle_state_signal.connect(
            self.system.change_tmp_pump_state)  # change_tmp_pump_opened
        self.system.change_tmp_pump_opened.connect(
            self.milw.pressure_block.pump_block.on_update_throttle_state_signal.emit)
        # self.milw.pressure_block.pump_block.update_throttle_state_signal\
        #     .connect(self.system.back_pressure_valve_controller.on_change_state)
        # self.system.throttle_state_effect.connect(
        #     self.milw.pressure_block.pump_block.on_update_throttle_state_signal.emit)
        #
        # self.system.throttle_current_pressure_effect.connect(
        #     self.milw.pressure_block.pump_block.throttle_info.update_current_signal.emit)
        #
        # self.milw.pressure_block.pump_block.throttle_info.on_update_target_signal \
        #     .connect(self.system.back_pressure_valve_controller.turn_on_regulation)
        # self.system.throttle_target_pressure_effect.connect(
        #     self.milw.pressure_block.pump_block.throttle_info.update_target_signal.emit)
        #######################

        # CURRENT

        self.milw.temperature_block.current_settings.set_current_block.\
            set_value_function = self.system.set_target_current
        self.system.target_current_effect.connect(
            self.milw.temperature_block.current_settings.set_current_block.set_value
        )

        self.system.actual_current_effect.connect(
            self.milw.temperature_block.current_settings.set_current_value
        )
        self.system.actual_voltage_effect.connect(
            self.milw.temperature_block.current_settings.set_voltage_value
        )

        self.system.is_power_current_source_effect.connect(
            self.milw.temperature_block.current_settings.set_current_block.on_update_is_power_signal.emit
        )
        self.milw.temperature_block.current_settings.set_current_block\
            .power_button.clicked.connect(self.system.current_source_controller.toggle_power)

        # RAMP
        self.milw.temperature_block.current_settings.rise_current_block\
            .on_ramp_press = self.system.on_ramp_press_start
        self.milw.temperature_block.current_settings.rise_current_block\
            .input_current.textEdited.connect(self.system.set_target_current_ramp_value)
        self.milw.temperature_block.current_settings.rise_current_block\
            .input_time.textEdited.connect(self.system.set_ramp_seconds)

        self.system.ramp_seconds_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block.left_time_signal.emit
        )
        self.system.target_current_ramp_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block.target_current_signal.emit
        )
        self.system.is_active_ramp_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block\
                .active_ramp_signal.emit
        )
        self.system.is_waiting_ramp_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block\
                .waiting_ramp_signal.emit
        )

        # PYROMETER ############
        # self.system.current_temperature_effect.connect(
        #     self.milw.temperature_block.set_actual_temperature
        # )
        self.system.current_temperature_effect.connect(
            self.milw.pressure_control_block.show_temperature.update_temperature_signal.emit
        )
        ########################

        # TEMPERATURE REGULATION ############
        # <target temperature>
        self.system.target_temperature_effect.connect(
            self.milw.pressure_control_block.set_temperature.target_temperature_signal.emit
        )
        self.milw.pressure_control_block.set_temperature.on_update_target_temperature_signal.connect(
            self.system.target_temperature_effect
        )
        # <speed>
        self.system.temperature_pid_speed_effect.connect(
            self.milw.pressure_control_block.set_speed.speed_signal.emit
        )
        self.milw.pressure_control_block.set_speed.on_update_speed_signal.connect(
            self.system.temperature_pid_speed_effect
        )
        # <power regulation>
        self.system.is_temperature_regulation_active_effect.connect(
            self.milw.pressure_control_block.set_temperature.active_regulation_signal.emit
        )
        self.milw.pressure_control_block.set_temperature.on_regulation_press_signal.connect(
            self.system.on_temperature_regulation_press
        )
        #####################################

        # VAKUMETR #############
        self.system.accurate_vakumetr_effect.connect(
            self.milw.pressure_control_block.show_pressure_block.update_pressure_signal.emit
        )
        ########################
        # PUMP BUTTON #############
        self.milw.pressure_control_block.pump.on_button_press_signal.connect(
            self.system.on_pump_press
        )
        # self.system.pump.connect(
        #     self.milw.pressure_control_block.show_pressure_block.update_pressure_signal.emit
        # )
        ########################
        # VENT BUTTON #############
        self.milw.pressure_control_block.vent.on_button_press_signal.connect(
            self.system.on_vent_press
        )
        ########################

        # PLOT ####################

        self.milw.temperature_block.current_settings.plot_block.set_settings(
            self.system.logger.get_array_log,
            self.system.log_parameters,
        )

    def _update_ui_values(self):
        pass
        # self.main_interface_layout_widget.temperature_block.current_settings.set_voltage_value(
        #     self.system.voltage_value
        # )

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QIntValidator

from coregraphene.conf import settings
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QLineEdit

from coregraphene.constants.components import BACK_PRESSURE_VALVE_CONSTANTS, BACK_PRESSURE_VALVE_STATE
from grapheneqtui.components import ButterflyButton, PumpButton, InfoColumnWidget, ParameterLatexLabel
from grapheneqtui.constants import BUTTERFLY_BUTTON_STATE, PUMP_BUTTON_STATE, LIGHT_GREEN, SHADOW_BLUR_RADIUS
from grapheneqtui.utils import StyleSheet

styles = StyleSheet({
    "container": {
        "name": "QWidget#valve_control_widget",
        # "max-height": "200px",
    },
    "container2": {
        # "name": "QWidget",
        # "width": '300px',
        # "min-width": '300px',
        # "width": '100%',
        # "max-width": "390px",
        "background-color": "rgb(255, 255, 255)",
        # "border-radius": "14px",
        # "max-height": "300px",
        # "padding": "2px",
    },
    "label": {
        "font-size": "18px",
        # "background-color": "green",
        # "min-width": '10px',
        "max-width": '80px',
        # "width": '60px',
        # "border-radius": "0px",
    },
    "label_t": {
        "font-size": "24px",
    },
    "input": {
        # "border-radius": "0px",
        "font-size": "22px",
        # "height": "24px",
        # "min-height": "24px",
        # "background-color": "rgb(210, 210, 210)",
        "background-color": LIGHT_GREEN,
        "width": "100%",
        # "max-width": "100px",
    },
})

# PUMPS_CONFIGURATION = settings.PUMPS_CONFIGURATION


class PumpInfoColumnWidget(InfoColumnWidget):
    down_latex_fon_size_mult = 1.1

    def get_label_text_format(self, value: float):
        s = "{:.1E}".format(value).lower()
        num, degree = s.split('e')
        formatted_value = f"{num}*10^{{{int(degree)}}}"
        return f"${formatted_value}$ {self.unit}"


class ShowActualSpeedBlock(ParameterLatexLabel):
    update_speed_signal = pyqtSignal(float)

    def __init__(self, parent=None, digits_round=0):
        super().__init__(parent=parent)
        self.update_speed_signal.connect(self._set_value)
        self._set_value(0.0)
        self.digits_round = digits_round

    def _set_value(self, value):
        self.value = value
        if self.value < 1:
            s = "{:.1E}".format(value).lower()
            num, degree = s.split('e')
            formatted_value = f"{num}*10^{{{int(degree)}}}"
        else:
            formatted_value = f"{round(self.value, self.digits_round)}"

        self.setText(f"Act V = ${formatted_value}$ Hz")


class SetTargetSpeedBlock(QWidget):
    target_speed_signal = pyqtSignal(int)
    on_update_target_speed_signal = pyqtSignal(int)
    update_actual_speed_signal = pyqtSignal(float)

    target_speed_value = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container2)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.bottom_layout = QHBoxLayout()

        self.label_1 = QLabel()
        self.label_1.setText("Set speed")
        self.label_1.setStyleSheet(styles.label)

        self.label_2 = QLabel()
        self.label_2.setText("%")
        self.label_2.setStyleSheet(styles.label)

        self.input = QLineEdit()
        self.input.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.input.setStyleSheet(styles.input)
        self.input.setValidator(QIntValidator(20, 100))
        self.bottom_layout.addWidget(self.label_1, stretch=1)
        self.bottom_layout.addWidget(self.input, stretch=4)
        self.bottom_layout.addWidget(self.label_2, 1)

        self.label_3 = QLabel()
        self.label_3.setText("Текущая уставка: ")

        self.label_4 = QLabel()
        self.label_4.setText("Actual speed: ")

        # self.bottom_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.layout.addLayout(self.bottom_layout, QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.label_3, alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label_4, alignment=QtCore.Qt.AlignHCenter)

        self.target_speed_signal.connect(self._set_target_speed)
        self.update_actual_speed_signal.connect(self._on_change_actual_speed)
        self.input.returnPressed.connect(self._on_update_input_value)

    def _on_update_input_value(self):
        try:
            input_value = self.input.text().replace(',', '.')
            value = int(input_value)
            self._on_change_target_speed(value)
            self.on_update_target_speed_signal.emit(value)
        except:
            self.input.setText('0')

    def _set_target_speed(self, value):
        self._on_change_target_speed(value)
        self.input.setText(str(value))

    def _on_change_target_speed(self, value):
        self.target_temperature_value = value
        print("New TARGET SPEED (%):", value)
        self.label_3.setText(f"Текущая уставка: {value}")

    def _on_change_actual_speed(self, value):
        # self.value = value
        if value < 1:
            # s = "{:.1E}".format(value).lower()
            # num, degree = s.split('e')
            # formatted_value = f"{num}*10^{{{int(degree)}}}"
            formatted_value = f"{round(value, 4)}"
        else:
            formatted_value = f"{round(value, 1)}"

        self.label_4.setText(f"Actual speed = {formatted_value} Hz")


class PumpsControlWidget(QWidget):
    # Base pump
    update_pump_state_signal = pyqtSignal()
    on_update_pump_is_open_signal = pyqtSignal(bool)

    # Pump TC110 ###
    update_pump_tc110_state_signal = pyqtSignal()
    on_update_pump_tc110_is_open_signal = pyqtSignal(bool)

    update_tc110_b_state_signal = pyqtSignal()
    on_update_tc110_b_state_signal = pyqtSignal(bool)

    # update_actual_speed_signal = pyqtSignal(float)
    update_target_speed_signal = pyqtSignal(int)
    on_update_target_speed_signal = pyqtSignal(int)

    ################

    update_pump_valve_state_signal = pyqtSignal()
    on_update_pump_valve_is_open_signal = pyqtSignal(bool)

    update_throttle_state_signal = pyqtSignal()
    on_update_throttle_state_signal = pyqtSignal(bool)

    confirmation_press_time_ms = 5000

    def __init__(self):
        super().__init__(parent=None)

        # TC110 #####
        self.pump_tc110_is_waiting = False
        self.pump_tc110_state = PUMP_BUTTON_STATE.CLOSE
        self.timer = QTimer(parent=None)
        #############

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setObjectName("valve_control_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.pump_button = PumpButton()
        self.pump_tc110_button = PumpButton()
        self.tc110_butterfly = ButterflyButton()

        self.label_t_symbol = QLabel('T', parent=self.pump_tc110_button)
        self.label_t_symbol.setStyleSheet(styles.label_t)

        self.label_t_symbol_b = QLabel('T', parent=self.tc110_butterfly)
        self.label_t_symbol_b.setStyleSheet(styles.label_t)

        self.pump_valve_b = ButterflyButton()
        self.throttle_b = ButterflyButton()

        self.throttle_info = PumpInfoColumnWidget(
            max_value=BACK_PRESSURE_VALVE_CONSTANTS.MAX_PRESSURE_BORDER,
            min_value=BACK_PRESSURE_VALVE_CONSTANTS.MIN_PRESSURE_BORDER,
            unit="mbar",
        )

        self.back_pressure_valve_layout = QHBoxLayout()
        self.back_pressure_valve_layout.addSpacing(2)
        # self.back_pressure_valve_layout.addWidget(
        #     self.throttle_info, stretch=2,
        #     alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        self.back_pressure_valve_layout.addWidget(
            self.throttle_b, stretch=2,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(
            self.pump_button, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        self.bottom_layout.addWidget(
            self.pump_valve_b, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)

        # PUMP TC110 #########################
        self.pump_tc110_layout = QHBoxLayout()
        self.pump_tc110_layout.addWidget(
            self.pump_tc110_button, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        self.pump_tc110_layout.addWidget(
            self.tc110_butterfly, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        speed_info_layout = QVBoxLayout()

        self.target_speed_block = SetTargetSpeedBlock()
        speed_info_layout.addWidget(self.target_speed_block)

        # self.tc110_actual_speed = ShowActualSpeedBlock()
        # speed_info_layout.addWidget(self.tc110_actual_speed)

        self.pump_tc110_layout.addLayout(speed_info_layout)
        ######################################

        # self.layout.addStretch(2)
        self.layout.addLayout(self.back_pressure_valve_layout)
        self.layout.addLayout(self.bottom_layout)
        self.layout.addLayout(self.pump_tc110_layout)

        self.on_update_pump_is_open_signal.connect(self._draw_pump_is_open)
        self.pump_button.clicked.connect(self._on_click_pump_button)

        self.on_update_pump_tc110_is_open_signal.connect(self._draw_pump_tc110_is_open)
        self.pump_tc110_button.clicked.connect(self._on_click_pump_tc110_button)

        self.on_update_pump_valve_is_open_signal.connect(self._draw_pump_valve_is_open)
        self.pump_valve_b.clicked.connect(self._on_click_pump_valve_butterfly)

        self.on_update_throttle_state_signal.connect(self._draw_throttle_state)
        self.throttle_b.clicked.connect(self._on_click_throttle_butterfly)

        self.on_update_tc110_b_state_signal.connect(self._draw_tc110_b_state)
        self.tc110_butterfly.clicked.connect(self._on_click_tc110_b_valve_butterfly)

    def _on_click_pump_button(self):
        self.update_pump_state_signal.emit()

    def _on_click_pump_tc110_button(self):  # update_pump_tc110_state_signal
        if self.pump_tc110_is_waiting or self.pump_tc110_state == PUMP_BUTTON_STATE.OPEN:
            self.update_pump_tc110_state_signal.emit()
            self.pump_tc110_is_waiting = False
        else:
            self.pump_tc110_is_waiting = True
            self.pump_tc110_button.update_state_signal.emit(PUMP_BUTTON_STATE.REGULATION)
            self.timer.singleShot(
                self.confirmation_press_time_ms,
                self._clear_button_waiting
            )

    def _clear_button_waiting(self):
        if self.pump_tc110_state == PUMP_BUTTON_STATE.OPEN:
            return
        self._draw_pump_tc110_is_open(False)

    def _on_click_pump_valve_butterfly(self):
        self.update_pump_valve_state_signal.emit()

    def _on_click_tc110_b_valve_butterfly(self):
        self.update_tc110_b_state_signal.emit()

    def _on_click_throttle_butterfly(self):
        self.update_throttle_state_signal.emit()

    def _draw_pump_is_open(self, is_open: bool):
        state = PUMP_BUTTON_STATE.OPEN if is_open else PUMP_BUTTON_STATE.CLOSE
        self.pump_button.update_state_signal.emit(state)

    def _draw_pump_tc110_is_open(self, is_open: bool):
        self.pump_tc110_is_waiting = False
        self.pump_tc110_state = PUMP_BUTTON_STATE.OPEN if is_open else PUMP_BUTTON_STATE.CLOSE
        self.pump_tc110_button.update_state_signal.emit(self.pump_tc110_state)

    def _draw_pump_valve_is_open(self, is_open: bool):
        state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
        self.pump_valve_b.update_state_signal.emit(state)

    def _draw_throttle_state(self, is_open: bool):
        state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
        self.throttle_b.update_state_signal.emit(state)

    def _draw_tc110_b_state(self, is_open: bool):
        state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
        self.tc110_butterfly.update_state_signal.emit(state)

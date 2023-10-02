from PyQt5.QtCore import pyqtSignal

from coregraphene.conf import settings
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from coregraphene.constants.components import BACK_PRESSURE_VALVE_CONSTANTS, BACK_PRESSURE_VALVE_STATE
from grapheneqtui.components import ButterflyButton, PumpButton, InfoColumnWidget
from grapheneqtui.constants import BUTTERFLY_BUTTON_STATE, PUMP_BUTTON_STATE
from grapheneqtui.utils import StyleSheet

styles = StyleSheet({
    "container": {
        "name": "QWidget#valve_control_widget",
        # "max-height": "200px",
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


class PumpsControlWidget(QWidget):
    update_pump_state_signal = pyqtSignal()
    on_update_pump_is_open_signal = pyqtSignal(bool)

    update_pump_valve_state_signal = pyqtSignal()
    on_update_pump_valve_is_open_signal = pyqtSignal(bool)

    update_throttle_state_signal = pyqtSignal()
    on_update_throttle_state_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__(parent=None)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setObjectName("valve_control_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.pump_button = PumpButton()

        self.pump_valve_b = ButterflyButton()
        self.throttle_b = ButterflyButton()

        self.throttle_info = PumpInfoColumnWidget(
            max_value=BACK_PRESSURE_VALVE_CONSTANTS.MAX_PRESSURE_BORDER,
            min_value=BACK_PRESSURE_VALVE_CONSTANTS.MIN_PRESSURE_BORDER,
            unit="mbar",
        )

        self.back_pressure_valve_layout = QHBoxLayout()
        self.back_pressure_valve_layout.addSpacing(2)
        self.back_pressure_valve_layout.addWidget(
            self.throttle_info, stretch=2,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        self.back_pressure_valve_layout.addWidget(
            self.throttle_b, stretch=2,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(
            self.pump_button, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        self.bottom_layout.addWidget(
            self.pump_valve_b, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)

        # self.layout.addStretch(2)
        self.layout.addLayout(self.back_pressure_valve_layout)
        self.layout.addLayout(self.bottom_layout)

        self.on_update_pump_is_open_signal.connect(self._draw_pump_is_open)
        self.pump_button.clicked.connect(self._on_click_pump_button)

        self.on_update_pump_valve_is_open_signal.connect(self._draw_pump_valve_is_open)
        self.pump_valve_b.clicked.connect(self._on_click_pump_valve_butterfly)

        self.on_update_throttle_state_signal.connect(self._draw_throttle_state)
        self.throttle_b.clicked.connect(self._on_click_throttle_butterfly)

    def _on_click_pump_button(self):
        self.update_pump_state_signal.emit()

    def _on_click_pump_valve_butterfly(self):
        self.update_pump_valve_state_signal.emit()

    def _on_click_throttle_butterfly(self):
        self.update_throttle_state_signal.emit()

    def _draw_pump_is_open(self, is_open: bool):
        state = PUMP_BUTTON_STATE.OPEN if is_open else PUMP_BUTTON_STATE.CLOSE
        self.pump_button.update_state_signal.emit(state)

    def _draw_pump_valve_is_open(self, is_open: bool):
        state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
        self.pump_valve_b.update_state_signal.emit(state)

    def _draw_throttle_state(self, state: int):
        valve_state = BUTTERFLY_BUTTON_STATE.INACTIVE
        if state == BACK_PRESSURE_VALVE_STATE.WAITING:
            valve_state = BUTTERFLY_BUTTON_STATE.INACTIVE
        elif state == BACK_PRESSURE_VALVE_STATE.OPEN:
            valve_state = BUTTERFLY_BUTTON_STATE.OPEN
        elif state == BACK_PRESSURE_VALVE_STATE.CLOSE:
            valve_state = BUTTERFLY_BUTTON_STATE.CLOSE
        elif state == BACK_PRESSURE_VALVE_STATE.REGULATION:
            valve_state = BUTTERFLY_BUTTON_STATE.REGULATION
        self.throttle_b.update_state_signal.emit(valve_state)

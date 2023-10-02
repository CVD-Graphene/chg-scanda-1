from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QHBoxLayout, QLineEdit

from grapheneqtui.components import LatexWidget
from .styles import styles

RGB = [175, 175, 250]


# class RampManager(QObject):
#     waiting_ramp_signal = pyqtSignal(bool)
#     active_ramp_signal = pyqtSignal(bool)
#     target_current_signal = pyqtSignal(float)
#     left_time_signal = pyqtSignal(int)


class RiseCurrentBlock(QWidget):
    on_ramp_press = None

    waiting_ramp_signal = pyqtSignal(bool)
    active_ramp_signal = pyqtSignal(bool)
    target_current_signal = pyqtSignal(float)
    left_time_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("rise_current_block")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.input_layout = QGridLayout()

        self.label_current = LatexWidget(
            text="$I_{final}$",
            rgb=RGB,
            top_y=0.9,
            # fon_size_mult=2
        )
        # self.label_current.setText("I_final")
        self.label_current.setStyleSheet(styles.label)

        self.label_current_1 = QLabel()
        self.label_current_1.setText("A")
        self.label_current_1.setStyleSheet(styles.label)
        self.label_current_1.setAlignment(QtCore.Qt.AlignLeft)

        self.label_time = LatexWidget(
            text="$t_{rise}$",
            rgb=RGB,
            top_y=0.8,
            # fon_size_mult=2
        )
        # self.label_time.setText("t_rise")
        self.label_time.setStyleSheet(styles.label)

        self.label_time_1 = QLabel()
        self.label_time_1.setText("s")
        self.label_time_1.setStyleSheet(styles.label)
        self.label_time_1.setAlignment(QtCore.Qt.AlignLeft)

        self.input_current = QLineEdit()
        self.input_current.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.input_current.setStyleSheet(styles.input)

        self.input_time = QLineEdit()
        self.input_time.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.input_time.setStyleSheet(styles.input)
        # self.input_time.textEdited()
        self.input_layout.addWidget(self.label_current, 0, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.input_layout.addWidget(self.input_current, 0, 1, QtCore.Qt.AlignBottom)
        self.input_layout.addWidget(self.label_current_1, 0, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.input_layout.addWidget(self.label_time, 1, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.input_layout.addWidget(self.input_time, 1, 1, QtCore.Qt.AlignTop)
        self.input_layout.addWidget(self.label_time_1, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # self.input_layout.setRowStretch(0, 10)
        # self.input_layout.setRowStretch(1, 100)

        ####################
        self.ramp_button = QPushButton()
        self.ramp_button.setText("RAMP")
        self.ramp_button.setStyleSheet(styles.button)
        self.ramp_waiting = False
        self.ramp_active = False

        self.layout.addLayout(self.input_layout, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.ramp_button,)

        self.ramp_button.clicked.connect(self._on_ramp_press)

        # self.ramp_manager = RampManager(parent=None)
        self.waiting_ramp_signal.connect(self._set_ramp_is_waiting)
        self.active_ramp_signal.connect(self._set_ramp_is_active)
        self.target_current_signal.connect(self._set_ramp_target_current)
        self.left_time_signal.connect(self._set_ramp_time)

    def _on_ramp_press(self):
        is_waiting = self.ramp_waiting
        self._set_ramp_is_waiting(True)
        if self.on_ramp_press and not is_waiting:
            self.on_ramp_press()

    def _set_ramp_is_waiting(self, is_waiting):
        self.ramp_waiting = is_waiting
        if self.ramp_waiting:
            self.ramp_button.setText("WAIT")
            self.ramp_button.setStyleSheet(styles.button_waiting)
        else:
            self._set_ramp_is_active(self.ramp_active)

    def _set_ramp_is_active(self, is_active):
        self.ramp_active = is_active
        if self.ramp_active:
            self.ramp_button.setText("STOP")
            self.ramp_button.setStyleSheet(styles.button_stop)
        else:
            self.ramp_button.setText("RAMP")
            self.ramp_button.setStyleSheet(styles.button)

    def _set_ramp_time(self, secs):
        self.input_time.setText(str(secs))

    def _set_ramp_target_current(self, value):
        self.input_current.setText(str(value))

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsDropShadowEffect, \
    QLineEdit, QLabel, QHBoxLayout, QBoxLayout, QSizePolicy, QPushButton

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .styles import styles


class SetTemperatureBlock(QWidget):
    target_temperature_signal = pyqtSignal(int)
    on_update_target_temperature_signal = pyqtSignal(int)
    active_regulation_signal = pyqtSignal(bool)
    on_regulation_press_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.regulation_active = False

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.title = QLabel()
        self.title.setText("Set temperature")
        self.title.setStyleSheet(styles.title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.bottom_layout = QHBoxLayout()

        self.label_1 = QLabel()
        self.label_1.setText("T =")
        self.label_1.setStyleSheet(styles.label)
        # self.label_1.setMaximumWidth(10)
        # self.label_1.setWordWrap(True)
        # sp_label_1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sp_label_1.setHorizontalStretch(1)
        # self.label_1.setSizePolicy(sp_label_1)

        self.label_2 = QLabel()
        self.label_2.setText("°C")
        self.label_2.setStyleSheet(styles.label)
        # sp_label_2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sp_label_2.setHorizontalStretch(2)
        # self.label_2.setSizePolicy(sp_label_2)

        self.input = QLineEdit()
        self.input.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.input.setStyleSheet(styles.input)
        # self.input.setMinimumWidth(1000)
        self.input.setValidator(QDoubleValidator(-10000.99, 10000.99, 2))
        # sp_input = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sp_input.setHorizontalStretch(20)
        # self.input.setSizePolicy(sp_input)
        # self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        # self.bottom_layout.setSpacing(0)

        # self.bottom_layout.addStretch(100)
        # self.bottom_layout.addStretch(100)
        # self.bottom_layout.addStretch(100)
        self.bottom_layout.addWidget(self.label_1, stretch=1)
        self.bottom_layout.addWidget(self.input, stretch=4)
        # self.bottom_layout.setStretch(0, 4)
        # # set a stretch factor of 1 for the second (the label)
        # self.bottom_layout.setStretch(1, 1)
        self.bottom_layout.addWidget(self.label_2, 1)

        ####################
        self.button = QPushButton()
        self.button.setText("START")
        self.button.setStyleSheet(styles.button)
        self.button.clicked.connect(self._on_button_press)

        # self.bottom_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.layout.addWidget(self.title, QtCore.Qt.AlignHCenter)
        self.layout.addLayout(self.bottom_layout, QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)

        self.active_regulation_signal.connect(self._set_regulation_is_active)
        self.target_temperature_signal.connect(self._set_target_temperature)
        self.input.returnPressed.connect(self._on_update_input_value)

    def _on_button_press(self):
        self.on_regulation_press_signal.emit()

    def _on_update_input_value(self):
        try:
            input_value = self.input.text().replace(',', '.')
            value = int(float(input_value))
            self.on_update_target_temperature_signal.emit(value)
        except:
            self.input.setText('0')

    def _set_regulation_is_active(self, is_active):
        self.regulation_active = is_active
        if self.regulation_active:
            self.button.setText("STOP")
            self.button.setStyleSheet(styles.button_stop)
        else:
            self.button.setText("START")
            self.button.setStyleSheet(styles.button)

    def _set_target_temperature(self, value):
        self.input.setText(str(value))

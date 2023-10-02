from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsDropShadowEffect, \
    QLineEdit, QLabel, QHBoxLayout, QBoxLayout, QSizePolicy, QPushButton

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .styles import styles


class PidSpeedBlock(QWidget):
    speed_signal = pyqtSignal(float)
    on_update_speed_signal = pyqtSignal(float)

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
        self.title.setText("Speed")
        self.title.setStyleSheet(styles.title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.bottom_layout = QHBoxLayout()

        self.label_1 = QLabel()
        self.label_1.setText("Ṫ =")
        self.label_1.setStyleSheet(styles.label)

        self.label_2 = QLabel()
        self.label_2.setText("c.u.")
        self.label_2.setStyleSheet(styles.label)

        self.input = QLineEdit()
        self.input.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.input.setStyleSheet(styles.input)
        self.input.setText('10.0')
        # self.input.setMinimumWidth(1000)
        # self.input.setValidator(QDoubleValidator(0, 100000.0, 2))

        self.bottom_layout.addWidget(self.label_1, stretch=1)
        self.bottom_layout.addWidget(self.input, stretch=4)
        self.bottom_layout.addWidget(self.label_2, 1)

        self.layout.addWidget(self.title, QtCore.Qt.AlignHCenter)
        self.layout.addLayout(self.bottom_layout, QtCore.Qt.AlignLeft)

        self.speed_signal.connect(self._set_speed)
        self.input.returnPressed.connect(self._on_update_input_value)

    def _on_update_input_value(self):
        try:
            input_value = self.input.text()#.replace(',', '.')
            value = min(10000.0, max(0.01, (float(input_value))))
            self.on_update_speed_signal.emit(value)
        except:
            self.input.setText('10.0')

    def _set_speed(self, value: float):
        value = str(value)#.replace('.', ',')
        self.input.setText(value)

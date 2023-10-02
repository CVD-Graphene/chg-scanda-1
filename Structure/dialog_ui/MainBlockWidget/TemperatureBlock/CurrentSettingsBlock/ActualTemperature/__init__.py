from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, QLabel

from .styles import styles


class ActualTemperature(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("actual_temperature_widget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # self.setGraphicsEffect(shadow)

        # self.temperature = ParameterLatexLabel()
        self.temperature = QLabel()
        self.temperature.setText("T = 300°C")
        self.temperature.setStyleSheet(styles.temperature)
        self.temperature.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.temperature, QtCore.Qt.AlignTop)

        self.label = QLabel()
        self.label.setText("Current source")
        self.label.setStyleSheet(styles.label)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label, )

    # def set_actual_temperature(self, value):
    #     self.temperature.setText(f"T = {value}°C")

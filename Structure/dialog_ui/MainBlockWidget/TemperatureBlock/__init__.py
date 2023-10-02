from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout

from .CurrentSettingsBlock import CurrentSettingsBlock
# from .SetTemperatureBlock import SetTemperatureBlock
from .styles import styles


class TemperatureBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("temperature_block_widget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # self.set_temperature = SetTemperatureBlock()
        # self.layout.addWidget(self.set_temperature, QtCore.Qt.AlignTop)

        self.current_settings = CurrentSettingsBlock()
        self.layout.addWidget(self.current_settings)

    # def set_actual_temperature(self, value):
    #     self.current_settings.set_actual_temperature(value)

from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout, QLineEdit

from grapheneqtui.components import ShowPressureBlock, ShowTemperatureBlock
from .FlowControlWidget import FlowControlWidget
from .PidSpeedBlock import PidSpeedBlock
# from .ShowPressureBlock import ShowPressureBlock
from .SetTemperatureBlock import SetTemperatureBlock
from .styles import styles


class PressureControlBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.show_pressure_block = ShowPressureBlock()
        self.layout.addWidget(self.show_pressure_block,
                              alignment=QtCore.Qt.AlignTop
                              )

        self.show_temperature = ShowTemperatureBlock()
        self.layout.addWidget(self.show_temperature,
                              alignment=QtCore.Qt.AlignTop
                              )

        # self.input = QLineEdit()
        # self.input.setStyleSheet("""
        # background-color: rgb(255, 255, 255);
        # max-width: 200px;
        # font-size: 24px;
        # """)
        # # self.input.clearFocus()
        # self.layout.addWidget(self.input)

        self.set_temperature = SetTemperatureBlock()
        self.layout.addWidget(self.set_temperature, alignment=QtCore.Qt.AlignTop)

        self.set_speed = PidSpeedBlock()
        self.layout.addWidget(self.set_speed, alignment=QtCore.Qt.AlignTop)

        self.pump = FlowControlWidget(title="Pump")
        self.vent = FlowControlWidget(title="Vent")
        self.layout.addWidget(self.pump, alignment=QtCore.Qt.AlignBottom)
        self.layout.addWidget(self.vent, alignment=QtCore.Qt.AlignBottom)

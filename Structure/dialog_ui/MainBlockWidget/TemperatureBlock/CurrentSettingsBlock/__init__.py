from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect

from pyqtgraph import PlotWidget
from PyQt5 import QtCore
import numpy as np
import pyqtgraph as pq

# from Structure.dialog_ui.components import ParameterLatexLabel, ParameterLabel
from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from grapheneqtui.components import ParameterLabel
from .ActualTemperature import ActualTemperature
from .PlotBlock import PlotBlock
from .RiseCurrentBlock import RiseCurrentBlock
from .SetCurrentBlock import SetCurrentBlock
from .styles import styles


class CurrentSettingsBlock(QWidget):
    get_plot_array_function = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("current_settings_block")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect(parent=None)
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.plot_block = PlotBlock()

        self.layout.addWidget(self.plot_block, alignment=QtCore.Qt.AlignTop)

        # self.actual_temperature = ActualTemperature()
        # self.layout.addWidget(self.actual_temperature, QtCore.Qt.AlignTop)

        self.set_current_block = SetCurrentBlock()
        self.layout.addWidget(self.set_current_block, )

        self.voltage_label = ParameterLabel()
        self.voltage_value = 0.0
        self.set_voltage_value(self.voltage_value)

        self.current_label = ParameterLabel()
        self.current_value = 0.0
        self.set_current_value(self.current_value)

        self.labels = QHBoxLayout()
        self.labels.addWidget(self.voltage_label, alignment=QtCore.Qt.AlignLeft)
        self.labels.addWidget(self.current_label, alignment=QtCore.Qt.AlignRight)

        self.layout.addLayout(self.labels, )
        self.rise_current_block = RiseCurrentBlock()
        self.layout.addWidget(self.rise_current_block, alignment=QtCore.Qt.AlignCenter)

    def set_voltage_value(self, value):
        self.voltage_value = float(value if str(value) else 0.0)
        self.voltage_label.setText(f"U = {round(self.voltage_value, 4)}V")

    def set_current_value(self, value):
        self.current_value = float(value if str(value) else 0.0)
        self.current_label.setText(f"I = {round(self.current_value, 3)}A")

    # def set_actual_temperature(self, value):
    #     self.actual_temperature.set_actual_temperature(value)

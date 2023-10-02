from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect, QComboBox

from pyqtgraph import PlotWidget
from PyQt5 import QtCore
import numpy as np
import pyqtgraph as pq


class PlotBlock(QWidget):
    """
    Plot block with choosing axes
    Example: https://www.programmersought.com/article/76756767412/
    """
    get_plot_array_function = None
    x_name = None
    y_name = None
    array_names = ['---']

    def __init__(self, parent=None, array_names=None):
        super().__init__(parent=parent)
        if array_names is not None:
            self.array_names = array_names

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.plotWidget_ted = PlotWidget()

        # Set the size and relative position of the control
        # self.plotWidget_ted.setGeometry(QtCore.QRect(25, 25, 550, 550))

        # Copy the data in the mode1 code
        # Generate 300 normally distributed random numbers
        # self.data1 = np.random.normal(size=300)
        # self.y = np.arange(300)
        # self.y[299] = 500
        # self.curve1 = self.plotWidget_ted.plot(self.y, self.data1, name="mode1")
        self.curve = self.plotWidget_ted.plot([0], [0], name="mode1")
        self.layout.addWidget(self.plotWidget_ted, alignment=QtCore.Qt.AlignTop)

        self.boxes_layout = QHBoxLayout()
        self.x_box = QComboBox()
        # self.x_box.addItems(self.array_names)
        # self.x_box.setCurrentIndex(0)
        self.x_box.currentTextChanged.connect(self.on_x_name_changed)

        self.y_box = QComboBox()
        # self.y_box.addItems(self.array_names)
        # y_index = 1 if len(self.array_names) > 1 else 0
        # self.y_box.setCurrentIndex(y_index)
        self.y_box.currentTextChanged.connect(self.on_y_name_changed)

        self.boxes_layout.addWidget(self.x_box, alignment=QtCore.Qt.AlignLeft)
        self.boxes_layout.addWidget(self.y_box, alignment=QtCore.Qt.AlignRight)

        self.layout.addLayout(self.boxes_layout)

        # Set timer
        self.timer = QTimer(parent=None)
        # Timer signal binding update_data function
        self.timer.timeout.connect(self.update_data)
        # The timer interval is 50ms, which can be understood as refreshing data once in 50ms
        self.timer.start(500)

    def on_x_name_changed(self, value):
        self.x_name = value
        self.update_data()

    def on_y_name_changed(self, value):
        self.y_name = value
        self.update_data()

    # Data shift left
    def update_data(self):
        if self.get_plot_array_function is None or \
                self.array_names is None or \
                len(self.array_names) <= 1 or \
                self.x_name is None or \
                self.y_name is None:
            return
        self.x = self.get_plot_array_function(self.x_name)
        self.y = self.get_plot_array_function(self.y_name)

        self.curve.setData(self.x, self.y)

    def set_settings(self, get_plot_array_function, array_names):
        self.get_plot_array_function = get_plot_array_function
        self.array_names = array_names

        self.x_box.addItems(self.array_names)
        self.y_box.addItems(self.array_names)
        self.x_box.setCurrentIndex(0)
        y_index = 1 if len(self.array_names) > 1 else 0
        self.y_box.setCurrentIndex(y_index)

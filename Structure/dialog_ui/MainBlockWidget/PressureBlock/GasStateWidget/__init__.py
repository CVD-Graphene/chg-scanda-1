from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, \
    QVBoxLayout, QLineEdit, QHBoxLayout, QLabel

from Structure.dialog_ui.components.butterfly_button import ButterflyButton
from .styles import styles


class GasStateWidget(QWidget):
    def __init__(self, gas="O2"):
        super().__init__()

        self.gas_name = gas

        self.line = QWidget(self)
        self.line.setStyleSheet(styles.line)
        self.line.setFixedWidth(self.width() - 120)
        # print("HEIGHT!!!", self.height() // 2) # 240 = h/2 ????
        self.line.move(120, 60)  # -self.height() // 2
        # self.layout.addWidget(self.line, QtCore.Qt.AlignAbsolute)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(styles.container)
        self.setObjectName("gas_state_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # self.line = QLineEdit()
        # self.layout.addWidget(self.line)

        # self.gas = QLabel()
        # self.gas = ParameterLatexLabel()
        self.gas = LatexWidget(
            text=f"${gas}$",
            rgb=[240, 240, 240],
            fon_size_mult=3.4
        )
        # self.gas.setText(gas)
        self.gas.setStyleSheet(styles.gas)
        # self.gas.setAlignment(QtCore.Qt.AlignCenter)

        self.b = ButterflyButton()

        self.up_label = QLabel()
        self.up_label.setText(f"0.0 sccm")
        self.up_label.setStyleSheet(styles.up_label)
        self.up_label.setAlignment(QtCore.Qt.AlignCenter)

        self.down_label = QLabel()
        self.down_label.setText(f"0.0 sccm")
        self.down_label.setStyleSheet(styles.down_label)
        self.down_label.setAlignment(QtCore.Qt.AlignCenter)

        self.info_layout_widget = QWidget()
        # self.info_layout_widget.setStyleSheet("background-color: #000000;max-height: 200px;")
        self.info_layout = QVBoxLayout()
        self.info_layout_widget.setLayout(self.info_layout)
        self.info_layout.addWidget(self.up_label, QtCore.Qt.AlignTop)
        self.info_layout.addWidget(self.down_label, QtCore.Qt.AlignTop)

        self.info_layout.setSpacing(0)
        # self.layout.setSpacing(0)

        self.layout.addWidget(self.gas, stretch=1, alignment=QtCore.Qt.AlignLeft)
        # self.layout.addStretch(10)
        self.layout.addWidget(self.info_layout_widget, stretch=1, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.b, stretch=10, alignment=QtCore.Qt.AlignHCenter,)

    def connect_valve_function(self, func):
        # self.valve_change_func = lambda : func(self.gas_name)
        # self.b.clicked.connect(self.valve_change_func)
        # self.b.on_click = lambda x: x

        def on_click():
            ans = func(self.gas_name)
            # print("GET ANS VALVE PRESS", ans)
            if type(ans) in [bool, int]:
                self.b._active = not ans
                self.b.paintEvent(event=None)

        self.b.clicked.connect(on_click)



class AirStateWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QWidget(self)
        self.line.setStyleSheet(styles.line)
        self.line.setFixedWidth(self.width() - 120)
        # print("HEIGHT!!!", self.height() // 2) # 240 = h/2 ????
        self.line.move(120, 60)  # -self.height() // 2
        # self.layout.addWidget(self.line, QtCore.Qt.AlignAbsolute)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setObjectName("gas_state_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.gas = QLabel()
        self.gas.setText("Air")
        self.gas.setStyleSheet(styles.gas)
        self.gas.setAlignment(QtCore.Qt.AlignCenter)

        self.b = ButterflyButton()

        self.label = QLabel()
        self.label.setText(f"1 bar")
        self.label.setStyleSheet(styles.down_label)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.gas, stretch=1, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.label, stretch=1, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.b, stretch=4, alignment=QtCore.Qt.AlignHCenter,)

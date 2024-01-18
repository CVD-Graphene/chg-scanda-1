from time import sleep
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, QLabel

from .buttons import ButtonPlus, ButtonMinus
from .digit import DigitLabel
from .styles import styles


class SetCurrentBlock(QWidget):
    on_update_is_power_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.value = 0.0
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setObjectName("set_current_block")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # self.setGraphicsEffect(shadow)

        ######################## LABELS ########################
        self.current_label = QLabel()
        self.current_label.setText("I=")
        self.current_label.setObjectName("current_label_local")
        self.current_label.setStyleSheet(styles.label)
        self.current_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.current_label.setFixedWidth(30)
        # self.layout.setColumnStretch(0, 10)
        # self.layout.setColumnStretch(1, 1000)
        self.layout.addWidget(self.current_label, 0, 0,)

        self.current_label_2 = QLabel()
        self.current_label_2.setText(",")
        self.current_label_2.setObjectName("current_label_local")
        self.current_label_2.setStyleSheet(styles.label)
        self.current_label_2.setFixedWidth(15)
        self.current_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.current_label_2, 0, 4,)

        self.current_label_3 = QLabel()
        self.current_label_3.setText("A")
        self.current_label_3.setObjectName("current_label_local")
        self.current_label_3.setStyleSheet(styles.label)
        self.current_label_3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.current_label_3, 0, 7,)

        self.is_power = True
        self.is_power_waiting = False
        self.on_update_is_power_signal.connect(self._on_update_is_power)

        power_layout = QVBoxLayout()

        self.power_button = QPushButton()
        self.power_button.setObjectName("power_button")
        self.power_button.setStyleSheet(styles.power_button)
        self.power_button.clicked.connect(self._on_press_power_button)
        # self.layout.addWidget(self.power_button, 0, 8, )
        power_layout.addWidget(self.power_button)
        power_layout.addWidget(QLabel('источник тока'))

        self.layout.addLayout(power_layout, 0, 8, )
        self._update_power_button_ui()

        # ################### DIGITS AND BUTTONS ###################### #

        # 100
        self.d1 = DigitLabel()
        self.layout.addWidget(self.d1, 0, 1)
        self.bp1 = ButtonPlus()
        self.bp1.clicked.connect(self.plus_100)
        self.layout.addWidget(self.bp1, 1, 1)
        self.bm1 = ButtonMinus()
        self.bm1.clicked.connect(self.minus_100)
        self.layout.addWidget(self.bm1, 2, 1)
        # 10
        self.d2 = DigitLabel()
        self.layout.addWidget(self.d2, 0, 2)
        self.bp2 = ButtonPlus()
        self.bp2.clicked.connect(self.plus_10)
        self.layout.addWidget(self.bp2, 1, 2)
        self.bm2 = ButtonMinus()
        self.bm2.clicked.connect(self.minus_10)
        self.layout.addWidget(self.bm2, 2, 2)
        # 1
        self.d3 = DigitLabel()
        self.layout.addWidget(self.d3, 0, 3)
        self.bp3 = ButtonPlus()
        self.bp3.clicked.connect(self.plus_1)
        self.layout.addWidget(self.bp3, 1, 3)
        self.bm3 = ButtonMinus()
        self.bm3.clicked.connect(self.minus_1)
        self.layout.addWidget(self.bm3, 2, 3)
        # 0.1
        self.d4 = DigitLabel()
        self.layout.addWidget(self.d4, 0, 5)
        self.bp4 = ButtonPlus()
        self.bp4.clicked.connect(self.plus_01)
        self.layout.addWidget(self.bp4, 1, 5)
        self.bm4 = ButtonMinus()
        self.bm4.clicked.connect(self.minus_01)
        self.layout.addWidget(self.bm4, 2, 5)
        # 0.01
        self.d5 = DigitLabel()
        self.layout.addWidget(self.d5, 0, 6)
        self.bp5 = ButtonPlus()
        self.bp5.clicked.connect(self.plus_001)
        self.layout.addWidget(self.bp5, 1, 6)
        self.bm5 = ButtonMinus()
        self.bm5.clicked.connect(self.minus_001)
        self.layout.addWidget(self.bm5, 2, 6)

        self.set_value()
        self.set_value_function = None

    def _on_update_is_power(self, is_power):
        self.is_power = is_power
        self.is_power_waiting = False
        self._update_power_button_ui()

    def _on_press_power_button(self):
        # self.is_power = not self.is_power
        if not self.is_power_waiting:
            self.is_power_waiting = True
            self._update_power_button_ui()

    def _update_power_button_ui(self):
        text = "OFF" if self.is_power else "ON"
        self.power_button.setText(text)
        if self.is_power_waiting:
            self.power_button.setStyleSheet(styles.waiting_power_button)
        else:
            self.power_button.setStyleSheet(styles.power_button)

    def set_real_value(self, value):
        # sleep(5)
        if value < 0.0:
            return
        if self.set_value_function is None:
            print("Current set_value_function is None!")
            return
        new_value = self.set_value_function(value)
        print("New current source ui value:", new_value)
        self.set_value(value=new_value)

    def set_value(self, value=None):
        # v = str(self.value)
        if value is None or type(value) not in [float, int]:
            pass
            # value = self.value
        else:
            self.value = round(value, 3)
        vi = int(self.value)
        self.d1.setText(str(vi // 100))
        self.d2.setText(str((vi % 100) // 10))
        self.d3.setText(str(vi % 10))
        self.d4.setText(str(int(self.value * 10) % 10))
        self.d5.setText(str(int(self.value * 100) % 10))

    def change_value(func):
        def wrapper(self):
            try:
                v1 = self.value
                func(self)
                # raise Exception("HOPA!!!")
                v2 = self.value
                letter = "." if v1 == v2 else "$"
                # print(f"|> {func.__name__}:\t{letter}\t{v1} => {v2}")
            except Exception as e:
                print("Err", e)
                # raise Exception("Ошибка установки значения тока: " + str(e))
        return wrapper

    ########### 100

    @change_value
    def plus_100(self):
        # d = int(self.value) // 100
        # if d == 9:
        #     return
        self.set_real_value(self.value + 100)
        # self.value += 100
        # self.d1.setText(str(d + 1))

    @change_value
    def minus_100(self):
        # d = int(self.value) // 100
        # if d == 0:
        #     return
        self.set_real_value(self.value - 100)
        # self.value -= 100
        # self.d1.setText(str(d - 1))

    ############## 10

    @change_value
    def plus_10(self):
        # d = (int(self.value) % 100) // 10
        # if d == 9:
        #     return
        self.set_real_value(self.value + 10)
        # self.value += 10
        # self.d2.setText(str(d + 1))

    @change_value
    def minus_10(self):
        # d = (int(self.value) % 100) // 10
        # if d == 0:
        #     return
        self.set_real_value(self.value - 10)
        # self.value -= 10
        # self.d2.setText(str(d - 1))

    ############ 1

    @change_value
    def plus_1(self):
        # d = int(self.value) % 10
        # if d == 9:
        #     return
        self.set_real_value(self.value + 1)
        # self.value += 1
        # self.d3.setText(str(d + 1))

    @change_value
    def minus_1(self):
        # d = int(self.value) % 10
        # if d == 0:
        #     return
        self.set_real_value(self.value - 1)
        # self.value -= 1
        # self.d3.setText(str(d - 1))

    ########### 0.1

    @change_value
    def plus_01(self):
        # d = int(self.value * 10) % 10
        # if d == 9:
        #     return
        self.set_real_value(self.value + 0.1)
        # self.value += 0.1
        # self.d4.setText(str(d + 1))

    @change_value
    def minus_01(self):
        # d = int(self.value * 10) % 10
        # if d == 0:
        #     return
        self.set_real_value(self.value - 0.1)
        # self.value -= 0.1
        # self.d4.setText(str(d - 1))

    ############# 0.01

    @change_value
    def plus_001(self):
        # d = int(self.value * 100) % 10
        # if d == 9:
        #     return
        self.set_real_value(self.value + 0.01)
        # self.value += 0.01
        # self.d5.setText(str(d + 1))

    @change_value
    def minus_001(self):
        # d = int(self.value * 100) % 10
        # if d == 0:
        #     return
        self.set_real_value(self.value - 0.01)
        # self.value -= 0.01
        # self.d5.setText(str(d - 1))

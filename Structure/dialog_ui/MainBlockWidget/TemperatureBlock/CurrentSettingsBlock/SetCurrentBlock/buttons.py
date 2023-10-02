from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS, LIGHT_GREEN
from coregraphene.ui import StyleSheet

side = "60px"

styles = StyleSheet({
    "container": {
        "name": "QPushButton#button_plus_minus",
        "height": side,
        "width": side,
        "background-color": "rgb(220, 255, 220)",
        # "border-style": "solid",
        "border-radius": "8px",
        # "border-width": "1px",
        # "border-color": "rgba(0,0,100,255)",
        "padding-left": "8px",
        "font-size": "24px",
        "text-align": "center",
    },
})

style_button = """
QPushButton#button_plus_minus {
    height: 60px;
    width: 60px;
    max-width: 60px;""" + \
               f"background-color: {LIGHT_GREEN};" + \
               """
                   font-size: 48px;
                   line-height: 48px;
               }
               QPushButton#button_plus_minus:pressed {
                   background-color: rgb(80, 200, 80);
               }
               """


class ButtonPlusMinus(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setText("?")
        self.setObjectName("button_plus_minus")
        self.setStyleSheet(style_button)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(2)
        self.setGraphicsEffect(shadow)


class ButtonPlus(ButtonPlusMinus):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setText("+")


class ButtonMinus(ButtonPlusMinus):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setText("-")

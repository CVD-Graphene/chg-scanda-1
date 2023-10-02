from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from coregraphene.ui import StyleSheet

side = "60px"

styles = StyleSheet({
    "container": {
        "name": "QLabel#digit_current_label",
        "height": side,
        "max-height": side,
        "width": side,
        "background-color": "rgb(255, 255, 255)",
        # "border-style": "solid",
        # "border-radius": "8px",
        # # "border-width": "1px",
        # # "border-color": "rgba(0,0,100,255)",
        # "padding-left": "8px",
        "font-size": "40px",
        # "text-align": "center",
    },
})

style_button = """
QPushButton#button_plus_minus {
    height: 60px;
    width: 60px;
    max-width: 60px;
    background-color: rgb(150, 255, 150);
    font-size: 48px;
    line-height: 48px;
}
QPushButton#button_plus_minus:pressed {
    background-color: rgb(80, 200, 80);
}
"""


class DigitLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()

        self.value = 1
        self.setText(str(self.value))
        self.setObjectName("digit_current_label")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setAlignment(QtCore.Qt.AlignCenter)

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(2)
        # self.setGraphicsEffect(shadow)


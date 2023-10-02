from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS, LIGHT_GREEN
from coregraphene.constants import NOTIFICATIONS
from grapheneqtui.utils import StyleSheet

WIDTH = "580px"
LABEL_WIDTH = "500px"

styles = StyleSheet({
    "container": {
        "max-height": "120px",
        "min-height": "120px",
        "min-width": WIDTH,
        "width": WIDTH,

        "max-width": WIDTH,
        # "width": '100%',
        # "background-color": "rgb(169, 222, 255)",
        "background-color": LIGHT_GREEN,
        # "border-style": "solid",
        "border-radius": "4px",
        # "border-width": "1px",
        # "border-color": "rgba(0,0,100,255)",
        # "padding-left": "8px",
        # "font-size": "28px",
        # "text-align": "center",
    },
    "error_log": {
        "background-color": "rgb(255, 127, 127)",
    },
    "label": {
        "font-size": "18px",
        # "background-color": "rgb(255, 255, 127)",
        # "text-align": "left",
        "color": "black",
        "width": LABEL_WIDTH,
        "max-width": LABEL_WIDTH,
        "min-width": LABEL_WIDTH,
    },
    "close_button": {
        "name": "QPushButton#close_log_button",
        "min-height": "50px",
        "max-height": "50px",
        "width": "50px",
        "max-width": '50px',
        "min-width": '50px',
        # "padding": "4px",
        "font-size": "34px",
        "background-color": 'rgb(255, 255, 255)',
    },
})


class LogWidget(QWidget):
    def __init__(self, on_close=None, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.math = LatexWidget("", parent=self)
        # self.layout.addWidget(self.math, alignment=QtCore.Qt.AlignCenter)

        # self.setAlignment(QtCore.Qt.AlignCenter)
        self.label = QLabel(wordWrap=True,)
        # self.label.resize(300, 100)
        # self.label.setText("Example")
        self.label.setStyleSheet(styles.label)
        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.close_button = QPushButton()
        self.close_button.setObjectName("close_log_button")
        self.close_button.setStyleSheet(styles.close_button)
        self.close_button.setText("X")
        self.close_button.clicked.connect(self.hide_log)
        self.layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)

        self.uid = None
        self.on_close = on_close

        shadow = QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # adding shadow to the label
        self.setGraphicsEffect(shadow)
        self.hide()

    def hide_log(self):
        if self.on_close is not None:
            self.on_close(self.uid)
        self.label.setText("")
        self.uid = None
        self.hide()

    def set_log(self, log):
        # print("SET LOG:", log)
        self.label.setText(log.log)
        self.uid = log.uid
        if log.log_type == NOTIFICATIONS.ERROR:
            self.setStyleSheet(styles.union('container', 'error_log'))
        else:
            self.setStyleSheet(styles.container)
        self.show()

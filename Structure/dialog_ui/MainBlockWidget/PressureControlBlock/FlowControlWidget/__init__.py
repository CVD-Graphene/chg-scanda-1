from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, \
    QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, QHBoxLayout

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .styles import styles, button_on_style, button_off_style, button_wait_style


class FlowControlWidget(QWidget):
    active_update_signal = pyqtSignal(bool)
    on_button_press_signal = pyqtSignal()
    confirmation_press_time_ms = 5000

    def __init__(self, title="Title"):
        super().__init__()

        self.button_ready = True
        self.button_wait = False

        self.timer = QTimer(parent=None)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.title = QLabel()
        self.title.setText(title)
        self.title.setStyleSheet(styles.title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.buttons = QHBoxLayout()
        self.button_on = QPushButton()
        self.button_on.setObjectName("button_on_flow")
        self.button_on.setStyleSheet(button_on_style)
        # self.button_off = QPushButton()
        # self.button_off.setStyleSheet(button_off_style)

        self.buttons.addWidget(self.button_on, alignment=QtCore.Qt.AlignHCenter)
        # self.buttons.addWidget(self.button_off)
        self.layout.addLayout(self.buttons)
        self.button_on.clicked.connect(self._on_button_press)

        self.active_update_signal.connect(self._set_button_is_active)
        self._update_button_ui()

    def _on_button_press(self):
        # if self.button_ready:
        if self.button_wait:
            self.on_button_press_signal.emit()
            # self.button_ready = False
            self.button_wait = False
        else:
            self.button_wait = True
            self.timer.singleShot(
                self.confirmation_press_time_ms,
                self._clear_button_waiting
            )
        # else:
        #     self.button_ready = False
        self._update_button_ui()

    def _update_button_ui(self):
        if self.button_ready:
            if self.button_wait:
                self.button_on.setStyleSheet(button_wait_style)
            else:
                self.button_on.setStyleSheet(button_on_style)
        else:
            self.button_on.setStyleSheet(button_off_style)

    def _set_button_is_active(self, is_active):
        self.button_on = is_active
        self.button_wait = False
        self._update_button_ui()

    def _clear_button_waiting(self):
        self.button_wait = False
        self._update_button_ui()

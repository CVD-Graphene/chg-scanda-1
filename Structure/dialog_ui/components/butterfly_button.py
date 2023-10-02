import math
from random import randint

from PyQt5 import QtCore
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout, QLineEdit
# from .styles import styles

SIDE = 60
SIN_SIDE = 60 * (3 ** 0.5) / 2
"""
    height: 60px;
    min-height: 100px;
    min-width: 120px;
    width: 100%;
"""
style_container = """
QPushButton#butterfly_button {
    height: 60px;
    min-width: 120px;
    margin: 0;
    padding: 0;
    background-color: rgba(150, 255, 150, 0);
}
"""


class ButterflyButton(QPushButton):
    def __init__(self):
        super().__init__()

        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setObjectName("butterfly_button")
        self.setStyleSheet(style_container)
        self._colors = {
            True: QColor(0, 255, 60),
            False: QColor(255, 0, 0)
        }
        self._active = False
        # self.clicked.connect(self.on_click)
        self.setContentsMargins(0,0,0,0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def on_click(self):
        self._active = not self._active
        self.paintEvent(event=None)

    def paintEvent(self, event):
        try:
            qp = QPainter()
            qp.begin(self)

            # a = randint(10, 100)
            # d = a * math.tan(math.radians(30))
            x, y = 0, 0

            pos_tl = QPointF(x, y)
            pos_bl = QPointF(x, y + SIDE)
            pos_center = QPointF(x + SIN_SIDE, y + SIDE * 0.5)
            pos_center2 = QPointF(x + SIN_SIDE, y + SIDE * 0.5 + 1)
            pos_tr = QPointF(x + SIN_SIDE * 2, y)
            pos_br = QPointF(x + SIN_SIDE * 2, y + SIDE)

            qp.setBrush(self._colors[self._active])
            path = QPainterPath()
            path.moveTo(pos_tl)
            path.lineTo(pos_center)
            path.lineTo(pos_tr)
            path.lineTo(pos_br)
            path.lineTo(pos_center2)
            path.lineTo(pos_bl)
            path.lineTo(pos_tl)

            qp.drawPath(path)

            qp.end()
        except Exception as e:
            print("Draw triangle error", e)

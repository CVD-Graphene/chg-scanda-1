from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout

from grapheneqtui.structures import RightButtonsWidget
from .recipe_buttons import RecipesButtonsWidget
from .styles import styles


class AppRightButtonsWidget(RightButtonsWidget):
    def __init__(self,
                 recipe_btns=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.recipe_btns = recipe_btns

    def on_open_recipe(self):
        self.recipe_btns.on_open()

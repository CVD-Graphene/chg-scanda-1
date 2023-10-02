from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout
from .styles import styles


class RightButtonsWidget(QWidget):
    def __init__(self,
                 on_close=None,
                 on_create_recipe=None,
                 on_open_recipe=None,
                 on_pause_recipe=None,
                 on_stop_recipe=None
                 ):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet("background-color: rgb(0, 0, 255);")

        self.button_close = QPushButton("CLOSE X")
        self.button_close.setObjectName("button_close")
        self.button_close.clicked.connect(on_close)
        self.button_close.setStyleSheet(styles.close_button)

        self.button_settings = QPushButton("SETTINGS")
        self.button_settings.setObjectName("settings_button")
        self.button_settings.setStyleSheet(styles.settings_button)

        self.select_recipe = QPushButton("Select and\nrun recipe")
        self.select_recipe.setObjectName("run_recipe_button")
        self.select_recipe.clicked.connect(on_open_recipe)
        self.select_recipe.setStyleSheet(styles.run_recipe_button)

        # self.select_recipe = QPushButton("Create\nrecipe")
        # self.select_recipe.setObjectName("run_recipe_button")
        # self.select_recipe.setStyleSheet(styles.run_recipe_button)

        self.edit_recipe = QPushButton("Create\nrecipe")
        self.edit_recipe.setObjectName("edit_recipe_button")
        self.edit_recipe.clicked.connect(on_create_recipe)
        self.edit_recipe.setStyleSheet(styles.edit_recipe_button)

        self.layout.addWidget(self.button_close, 0, 0, QtCore.Qt.AlignTop)
        # self.right_buttons_layout.setRowMinimumHeight(0, 10)
        # self.right_buttons_layout.setRowStretch(0, 10)

        self.layout.addWidget(self.button_settings, 1, 0, QtCore.Qt.AlignTop)
        self.layout.setRowMinimumHeight(1, 100)
        # self.right_buttons_layout.setRowStretch(1, 1)

        self.manage_recipe_layout = QVBoxLayout()

        self.pause_recipe = QPushButton("PAUSE")
        self.pause_recipe.setObjectName("pause_recipe_button")
        if on_pause_recipe:
            self.pause_recipe.clicked.connect(on_pause_recipe)
        self.pause_recipe.setStyleSheet(styles.pause_recipe_button)

        self.stop_recipe = QPushButton("STOP")
        self.stop_recipe.setObjectName("stop_recipe_button")
        if on_stop_recipe:
            self.stop_recipe.clicked.connect(on_stop_recipe)
        self.stop_recipe.setStyleSheet(styles.stop_recipe_button)

        self.layout.addWidget(self.select_recipe, 2, 0)
        self.layout.addWidget(self.edit_recipe, 3, 0)

        self.layout.addWidget(self.pause_recipe, 4, 0)
        self.layout.addWidget(self.stop_recipe, 5, 0)

        self.stop_recipe.hide()
        self.pause_recipe.hide()

    def activate_manage_recipe_buttons(self):
        self.select_recipe.hide()
        self.button_settings.hide()
        self.edit_recipe.hide()

        self.pause_recipe.show()
        self.stop_recipe.show()

    def deactivate_manage_recipe_buttons(self):
        self.select_recipe.show()
        self.button_settings.show()
        self.edit_recipe.show()

        self.pause_recipe.hide()
        self.stop_recipe.hide()

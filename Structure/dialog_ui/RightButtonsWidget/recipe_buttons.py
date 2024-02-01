import os
import uuid

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QFileDialog, \
    QTableWidget, QLineEdit, QPushButton, QHBoxLayout, QHeaderView
from PyQt5.QtCore import QSize

from .styles import styles


custom_font = QFont()
custom_font.setPointSize(18)


class RecipesButtonsWidget(QWidget):

    def __init__(self,
                 parent=None,
                 on_open_recipe=None,
                 on_run_recipe_by_file=None,
                 ):
        super().__init__(parent)

        self.material = None
        self.material_row = True

        self._on_run_recipe_by_file = on_run_recipe_by_file
        self._on_open_recipe = on_open_recipe

        self.file = None
        self.path = None

        self.file_path = None  # for directly open files

        self.setObjectName("RecipesButtonsWidget")
        self.setStyleSheet(styles.recipes_buttons_widget)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.grid_layout = QGridLayout()  # Create QGridLayout
        self.setLayout(self.grid_layout)
        # QApplication.desktop().width(),
        # QApplication.desktop().height()

        self.setFont(custom_font)

        self.setMinimumSize(QSize(
            int(QApplication.desktop().width() * 0.9),
            int(QApplication.desktop().height() * 0.8)
        ))  # Set sizes
        self.setMaximumWidth(int(QApplication.desktop().width() * 0.9))

        #######################

        self.nickel_btn = QPushButton('Никель')
        self.nickel_btn.setStyleSheet(styles.choose_recipe_button)
        self.nickel_btn.clicked.connect(self.on_nickel)

        self.iron_btn = QPushButton('Железо')
        self.iron_btn.setStyleSheet(styles.choose_recipe_button)
        self.iron_btn.clicked.connect(self.on_iron)

        self.copper_btn = QPushButton('Медь')
        self.copper_btn.setStyleSheet(styles.choose_recipe_button)
        self.copper_btn.clicked.connect(self.on_copper)

        self.modes_layout = QHBoxLayout()

        self.modes_layout.addWidget(self.nickel_btn)
        self.modes_layout.addWidget(self.iron_btn)
        self.modes_layout.addWidget(self.copper_btn)

        #######################

        #######################

        self.rec_back = QPushButton('Назад')
        self.rec_back.setStyleSheet(styles.choose_recipe_button)
        self.rec_back.clicked.connect(self.on_numbers_back)

        self.rec_1 = QPushButton('#1')
        self.rec_1.setStyleSheet(styles.choose_recipe_button)
        self.rec_1.clicked.connect(self.on_rec_1)
        self.rec_2 = QPushButton('#2')
        self.rec_2.setStyleSheet(styles.choose_recipe_button)
        self.rec_2.clicked.connect(self.on_rec_2)
        self.rec_3 = QPushButton('#3')
        self.rec_3.setStyleSheet(styles.choose_recipe_button)
        self.rec_3.clicked.connect(self.on_rec_3)
        self.rec_4 = QPushButton('#4')
        self.rec_4.setStyleSheet(styles.choose_recipe_button)
        self.rec_4.clicked.connect(self.on_rec_4)
        self.rec_5 = QPushButton('#5')
        self.rec_5.setStyleSheet(styles.choose_recipe_button)
        self.rec_5.clicked.connect(self.on_rec_5)

        self.numbers_layout = QHBoxLayout()

        # self.numbers_layout.addWidget(self.rec_back)
        self.modes_layout.addWidget(self.rec_1)
        self.modes_layout.addWidget(self.rec_2)
        self.modes_layout.addWidget(self.rec_3)
        self.modes_layout.addWidget(self.rec_4)
        self.modes_layout.addWidget(self.rec_5)
        self.rec_1.hide()
        self.rec_2.hide()
        self.rec_3.hide()
        self.rec_4.hide()
        self.rec_5.hide()

        #######################

        buttons_layout = QHBoxLayout()

        close_button = QPushButton("CLOSE")
        close_button.clicked.connect(self.on_close)
        close_button.setObjectName("table_button")
        close_button.setStyleSheet(styles.table_button)

        start_button = QPushButton("OPEN RECIPE")
        start_button.clicked.connect(self.on_run_recipe)
        start_button.setObjectName("table_button")
        start_button.setStyleSheet(styles.table_button)

        # buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(close_button)

        self.grid_layout.addLayout(buttons_layout, 0, 0)
        self.grid_layout.addLayout(self.modes_layout, 1, 0)

        self._update_table()
        self.hide()

    def on_run_recipe(self):
        self.on_close()
        self._on_run_recipe()

    def _update_table_ui(self):
        pass

    def on_numbers_back(self):
        pass

    def on_open(self):
        self.show()

    def on_nickel(self):
        self.material = "nickel"
        self.on_choose_material()

    def on_iron(self):
        self.material = "iron"
        self.on_choose_material()

    def on_copper(self):
        self.material = "copper"
        self.on_choose_material()

    def on_rec_1(self):
        self.on_rec_run(1)

    def on_rec_2(self):
        self.on_rec_run(2)

    def on_rec_3(self):
        self.on_rec_run(3)

    def on_rec_4(self):
        self.on_rec_run(4)

    def on_rec_5(self):
        self.on_rec_run(5)

    def on_rec_run(self, file_nun):
        path = os.path.join('recipes', self.material, f"recipe_{file_nun}.xlsx")
        self._on_run_recipe_by_file(path)
        self.on_close()

    def on_choose_material(self):
        self.nickel_btn.hide()
        self.iron_btn.hide()
        self.copper_btn.hide()

        self.rec_1.show()
        self.rec_2.show()
        self.rec_3.show()
        self.rec_4.show()
        self.rec_5.show()

    def set_target_file(self, path=None, file=None):
        self.file = file
        self.path = path

    def _update_table(self):
        pass
        self._update_table_ui()

    def on_close(self):
        self.nickel_btn.show()
        self.iron_btn.show()
        self.copper_btn.show()

        self.rec_1.hide()
        self.rec_2.hide()
        self.rec_3.hide()
        self.rec_4.hide()
        self.rec_5.hide()

        self.file = None
        self.path = None
        self.file_path = None
        self.hide()

        self._update_table()

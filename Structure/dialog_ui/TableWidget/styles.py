from coregraphene.ui import StyleSheet
from Structure.dialog_ui.constants import LIGHT_GREEN

BUTTON_HEIGHT = "48px"

styles = StyleSheet({
    "container": {
        "name": "QWidget#AppTableWidget",
        # "max-width": "240px",
        # "min-width": "180px",
        "background-color": "rgb(50, 50, 50)",
    },
    "table_button": {
        "name": "QPushButton#table_button",
        "height": BUTTON_HEIGHT,
        "font-size": "20px",
        # "background-color": "rgb(255, 150, 150)",
    },
    "table_name_input": {
        "name": "QLineEdit#table_name_input",
        "height": BUTTON_HEIGHT,
        "max-width": "500px",
        "min-width": "500px",
        "width": "500px",
        "font-size": "20px",
        # "background-color": "rgb(255, 255, 230)",
    },
    "run_recipe_button": {
        "name": "QPushButton#run_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": LIGHT_GREEN,
    },
    "edit_recipe_button": {
        "name": "QPushButton#edit_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": LIGHT_GREEN,
    },
})

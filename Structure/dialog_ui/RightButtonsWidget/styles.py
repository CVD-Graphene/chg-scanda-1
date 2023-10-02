from coregraphene.ui import StyleSheet
from Structure.dialog_ui.constants import LIGHT_GREEN


styles = StyleSheet({
    "container": {
        # "name": "QWidget",
        "max-width": "240px",
        "min-width": "180px",
        # "background-color": "rgb(150, 250, 250)",
    },
    "close_button": {
        "name": "QPushButton#button_close",
        "height": "70px",
        "font-size": "20px",
        "background-color": "rgb(255, 150, 150)",
    },
    "settings_button": {
        "name": "QPushButton#settings_button",
        "height": "70px",
        "font-size": "20px",
        "background-color": "rgb(255, 255, 230)",
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
    "pause_recipe_button": {
        "name": "QPushButton#pause_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": 'rgb(255, 255, 0)',
    },
    "stop_recipe_button": {
        "name": "QPushButton#stop_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": 'rgb(255, 0, 0)',
    },
})

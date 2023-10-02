from coregraphene.ui import StyleSheet
from Structure.dialog_ui.constants import LIGHT_GREEN

styles = StyleSheet({
    "container": {
        "name": "QWidget#actual_temperature_widget",
        # "min-width": "300px",
        # "height": "100%",
        "max-height": "200px",
        "border-style": "solid",
        # "border-radius": "8px",
        "border-width": "2px",
        "border-color": "rgb(0, 0, 50)",
        # "background-color": "rgb(138, 181, 255)",
    },
    "temperature": {
        # "border-width": "0",
        "font-size": "42px",
        # "background-color": LIGHT_GREEN,
        "background-color": "rgba(220, 220, 220, 255)",
        "padding": "6px",
    },
    "label": {
        # "border-width": "0",
        "font-size": "32px",
        "font-weight": "bold",
        "background-color": "rgba(0, 0, 0, 0)",
    },
})

from coregraphene.ui import StyleSheet
from Structure.dialog_ui.constants import LIGHT_GREEN

styles = StyleSheet({
    "container": {
        "name": "QWidget#rise_current_block",
        # "min-width": "300px",
        # "height": "100%",
        "max-height": "190px",
        # "border-style": "solid",
        # # "border-radius": "8px",
        # "border-width": "2px",
        # "border-color": "rgb(0, 0, 50)",
        # "background-color": "rgb(198, 181, 255)",
    },
    "input": {
        "font-size": "32px",
        # "background-color": "rgb(220, 220, 255)",
        "max-width": "200px",
        # "background-color": "rgba(220, 220, 220, 255)",
        # "padding": "6px",
    },
    "label": {
        # "name": "QLabel#",
        "min-width": "100px",
        # "max-width": "40px",
        # "border-width": "0",
        "min-height": "40px",
        "font-size": "32px",
        # "font-weight": "bold",
        # "background-color": "rgba(0, 0, 0, 0)",
    },
    "button": {
        "height": '100%',
        "min-height": "100px",
        "min-width": "150px",
        "padding": "10px",
        "font-size": "32px",
        "background-color": LIGHT_GREEN,
    },
    "button_waiting": {
        "height": '100%',
        "min-height": "100px",
        "min-width": "150px",
        "padding": "10px",
        "font-size": "32px",
        "background-color": 'rgb(253, 239, 43)',
    },
    "button_stop": {
        "height": '100%',
        "min-height": "100px",
        "min-width": "150px",
        "padding": "10px",
        "font-size": "32px",
        "background-color": 'rgb(253, 94, 45)',
    },
})

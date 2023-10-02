from coregraphene.ui import StyleSheet

GAS_HEIGHT = "100px"

styles = StyleSheet({
    "container": {
        "name": "QWidget#gas_state_widget",
        "max-height": "120px",
        # "max-width": "5000px",
        # "width": "100%",
        # "height": '100%',
        # "background-color": "rgb(0, 240, 0)",
    },
    "gas": {
        # "width": "70px",
        # "width": "100%",
        # "background-color": "rgb(0, 240, 255)",
        "max-height": GAS_HEIGHT,
        "min-height": GAS_HEIGHT,
        "height": GAS_HEIGHT,
        "min-width": "80px",
        "font-size": "48px",
        "font-weight": "bold",
    },
    "up_label": {
        "max-height": "60px",
        "min-width": "180px",
        # "width": "120px",
        "background-color": "rgb(255, 255, 255)",
        "font-size": "28px",
    },
    "down_label": {
        "max-height": "60px",
        "min-width": "180px",
        # "width": "120px",
        "background-color": "rgb(180, 180, 180)",
        "font-size": "28px",
    },
    "line": {
        "height": "2px",
        "max-height": "2px",
        "width": "100%",
        "background-color": "rgb(0, 0, 0)",
        # "position": "absolute",
        # "left": "0",
        # "right": "0",
    }
})

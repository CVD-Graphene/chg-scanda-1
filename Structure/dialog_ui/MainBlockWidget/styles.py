from coregraphene.ui import StyleSheet

styles = StyleSheet({
    "container": {
        "name": "QWidget#main_block_widget",
        # "width": "100%",
        # "background-color": "rgb(220, 220, 255)",
    },
    "inactive_widget": {
        "name": "QWidget#inactive_widget",
        "width": '20000px',
        "min-width": '20000px',
        'height': '20000px',
        'min-height': '20000px',
        # 'opacity': '0.5',
        'background-color': "rgba(200, 200, 200, 0.2)",
    }
})

# print(styles.container)

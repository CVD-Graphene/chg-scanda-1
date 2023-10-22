from coregraphene.conf import settings
from grapheneqtui.structures import BaseMainBlockWidget
# from .PressureBlock import PressureBlock, ValvesControlBlock
from .PressureBlock import ValvesControlBlock
from .PressureControlBlock import PressureControlBlock
from .TemperatureBlock import TemperatureBlock
from .styles import styles


class MainBlockWidget(BaseMainBlockWidget):

    def set_layout_content(self):
        self.pressure_block = ValvesControlBlock(
            gases_configuration=settings.VALVES_CONFIGURATION,
            default_sccm_value=settings.MAX_DEFAULT_SCCM_VALUE,
        )
        self.layout.addWidget(self.pressure_block)

        self.pressure_control_block = PressureControlBlock()
        self.layout.addWidget(self.pressure_control_block)

        self.temperature_block = TemperatureBlock()
        self.layout.addWidget(self.temperature_block)

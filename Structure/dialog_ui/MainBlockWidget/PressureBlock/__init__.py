from grapheneqtui.structures import BaseValvesControlBlock
from .PumpsControl import PumpsControlWidget


class ValvesControlBlock(BaseValvesControlBlock):
    def set_control_valves(self):
        self.pump_block = PumpsControlWidget()
        self.layout.addWidget(self.pump_block)

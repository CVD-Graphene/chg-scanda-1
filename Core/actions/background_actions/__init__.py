from coregraphene.actions import BaseBackgroundAction
from ..actions import TemperatureRegulationAction


class PidTemperatureBackgroundAction(BaseBackgroundAction):
    action_class = TemperatureRegulationAction

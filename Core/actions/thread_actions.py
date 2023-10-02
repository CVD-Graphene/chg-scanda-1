from coregraphene.actions import BaseThreadAction
from .actions import RampAction


class RampThreadAction(BaseThreadAction):
    action = RampAction

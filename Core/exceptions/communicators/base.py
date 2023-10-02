import datetime


class BaseCommunicatorException(Exception):
    def __init__(self, communicator_id=None):
        self.communicator_id = communicator_id
        self.description = f"Communicator raise exception"
        self.raised_at = datetime.datetime.now()

    def __str__(self):
        communicator_str = "Communicator"
        if self.communicator_id:
            communicator_str += f" id={self.communicator_id}"
        return f"[ERROR {communicator_str}] {self.raised_at} - {self.description}"


class InactiveCommunicatorException(BaseCommunicatorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = f"Inactive communicator"


class SetupCommunicatorException(BaseCommunicatorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = f"Communicator setup error"

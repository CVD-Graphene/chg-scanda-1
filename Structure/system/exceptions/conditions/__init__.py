from coregraphene.exceptions import BaseConditionException


class BadNumbersConditionException(BaseConditionException):
    def __init__(self):
        super().__init__("Bad numbers")

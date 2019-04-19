from enum import IntEnum

class State(IntEnum):
    START = 1
    SELECT_PLAN = 2
    SELECT_PAYMENT = 3
    PAY_BTC = 4
    PAY_NEO = 5
    ACCEPTED = 6
    CANCELED = 7

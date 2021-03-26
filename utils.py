from enum import Enum, auto


class State(Enum):
    WAITING_FOR_START = auto()
    WAITING_IN_STOP = auto()
    MOVING = auto()

class Way(Enum):
    UP = auto()
    DOWN = auto()
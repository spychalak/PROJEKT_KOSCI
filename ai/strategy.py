from enum import Enum, auto

class Strategy(Enum):
    SAFE_SCORE = auto()
    HUNT_GENERAL = auto()
    HUNT_FOUR_KIND = auto()
    HUNT_FULL_HOUSE = auto()
    HUNT_STRAIGHT = auto()
    DUMP_BAD = auto()
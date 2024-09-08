from enum import Enum

class Mode(Enum):
    ROUND_NEAREST_TIES_EVEN = 0 # NOT CURRENTLY SUPPORTED
    ROUND_NEAREST_TIES_AWAY = 1 # NOT CURRENTLY SUPPORTED
    ROUND_UP = 2 # NOT CURRENTLY SUPPORTED
    ROUND_DOWN = 3
    # TODO: difference between truncate and round down
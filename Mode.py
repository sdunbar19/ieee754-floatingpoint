from enum import Enum

class Mode(Enum):
    ROUND_NEAREST_TIES_EVEN = 0 # NOT CURRENTLY SUPPORTED
    ROUND_NEAREST_TIES_AWAY = 1 # NOT CURRENTLY SUPPORTED
    ROUND_UP = 2 # NOT CURRENTLY SUPPORTED
    ROUND_DOWN = 3 # NOT CURRENTLY SUPPORTED
    NO_ROUND = 4
    # currently, only mode supported is we don't round
    # min and max overflows are respected within bounds sans rounding (eg max is (2 - 2**-23) * 2**127, min is 2**-126)
    # if outside of bounds, is treated as overflow or underflow regardless of rounding
    # if in bounds, we "chop off" the extra part (e.g truncate)
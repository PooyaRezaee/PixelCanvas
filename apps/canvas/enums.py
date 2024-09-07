from enum import Enum


class Color(
    Enum
):  # NOTE: For now, eight colors are selected so that the colors can be stored in 3 bytes
    BLACK = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5
    CYAN = 6
    MAGENTA = 7
    UNKNOWN = -1
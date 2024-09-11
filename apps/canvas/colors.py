from .enums import Color

color_to_hex = {
    Color.BLACK: "#000000",
    Color.WHITE: "#FFFFFF",
    Color.RED: "#FF0000",
    Color.GREEN: "#00FF00",
    Color.BLUE: "#0000FF",
    Color.YELLOW: "#FFFF00",
    Color.CYAN: "#00FFFF",
    Color.MAGENTA: "#FF00FF",
}
num_to_enum = {
    0: Color.BLACK,
    1: Color.WHITE,
    2: Color.RED,
    3: Color.GREEN,
    4: Color.BLUE,
    5: Color.YELLOW,
    6: Color.CYAN,
    7: Color.MAGENTA,
}


def get_hex_color(color: Color) -> str:
    return color_to_hex.get(color, "#FFFFFF")


def get_enum_color(number: int) -> Color:
    return num_to_enum.get(number, Color.UNKNOWN)

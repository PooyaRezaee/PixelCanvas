from core import logger
from ..enums import Color
from ..colors import get_hex_color
from ..repositories.redis_operation import get_canvas, get_pixel_range


def show_canvas() -> list[tuple[int, int, str]]:
    """
    return list of pixels, each pixel is a tuple and have 'x, y, color'
    """
    return list(get_canvas())


def show_pixel_range(
    start_pixel: tuple[int, int], end_pixel: tuple[int, int]
) -> list[tuple[int, int, str]]:
    """
    argument is tuple of x and y coordinates
    """
    x_start, x_end = start_pixel
    y_start, y_end = end_pixel

    if x_start > x_end:
        raise ValueError(
            "The coordinates of the start pixel cannot be more x than the end pixel"
        )
    if y_start > y_end:
        raise ValueError(
            "The coordinates of the start pixel cannot be more y than the end pixel"
        )

    canvas = get_pixel_range(x_start, x_end, y_start, y_end)
    return canvas

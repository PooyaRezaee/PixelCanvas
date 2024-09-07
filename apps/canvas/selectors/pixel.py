from core import logger
from ..enums import Color
from ..colors import get_hex_color
from ..repositories.redis_operation import get_canvas, get_pixel


def show_canvas() -> list[tuple[int, int, str]]:
    """
    return list of pixels, each pixel is a tuple and have 'x, y, color'
    """
    return list(get_canvas())


def show_part_of_canvas(
    start_pixel: tuple[int, int], end_pixel: tuple[int, int]
) -> list[tuple[int, int, str]]:
    """
    argument is tuple of x and y coordinates
    """
    x_start, y_start = start_pixel
    x_end, y_end = end_pixel

    if x_start >= x_end:
        raise ValueError(
            "The coordinates of the start pixel cannot be more x than the end pixel"
        )
    if y_start >= y_end:
        raise ValueError(
            "The coordinates of the start pixel cannot be more y than the end pixel"
        )

    canvas = []
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            try:
                color = int(get_pixel(x, y))
            except ValueError:
                continue
            except Exception as e:
                logger.error(e)
                continue

            canvas.append((x, y, color))
    return canvas

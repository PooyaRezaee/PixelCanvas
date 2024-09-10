from core import logger
from ..enums import Color
from ..colors import get_hex_color
from ..repositories.redis_operation import get_canvas, get_pixel, r


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

    xs = range(x_start, x_end + 1)
    ys = range(y_start, y_end + 1)
    pipeline = r.pipeline()
    for x in xs:
        for y in ys:
            try:
                get_pixel(x, y, pipeline)
            except ValueError:
                continue
            except Exception as e:
                logger.error(e)
                continue

    result = pipeline.execute()
    canvas = []
    color_index = -1
    for x in xs:
        for y in ys:
            color_index += 1
            if result[color_index] is None:
                continue
            canvas.append((x, y, int(result[color_index].decode())))

    return canvas

from ..enums import Color
from ..repositories.redis_operation import save_pixel


def paint_pixel(x: int, y: int, color: Color) -> bool:
    if type(color) != Color:
        raise ValueError("color must be enum of canvas.enums.Color")
    
    try:
        save_pixel(x, y, color.value)
        return True
    except Exception:
        return False

import redis
from django.conf import settings
from core import logger

r = redis.from_url(settings.REDIS_LOCATION)


def save_pixel(x, y, color):
    try:
        key = f"pixel:{x}:{y}"
        r.set(key, color)
    except redis.RedisError as e:
        logger.error(f"Error saving pixel: {e}")
        raise


def get_pixel(x: str | int, y: str | int) -> int:
    try:
        key = f"pixel:{x}:{y}"
        color = r.get(key)
        if color is None:
            raise ValueError(f"Pixel at ({x}, {y}) not found.")
        if not color.decode().isdigit():
            raise TypeError(f"Color data for key {key} not's digit.")
        return int(color.decode())
    except redis.RedisError as e:
        logger.error(f"Error retrieving pixel: {e}")
        raise
    except AttributeError:
        logger.error(f"Error decoding pixel color for ({x}, {y})")
        raise
    except ValueError as e:
        logger.error(e)
        raise


def get_canvas() -> list[tuple[int, int, str]]:
    canvas = set()
    try:
        keys = r.keys("pixel:*")
        for key in keys:
            x, y = key.decode().split(":")[1:]
            color = r.get(key)
            if color is None:
                logger.warning(f"Color data for key {key} not found.")
                continue
            else:
                if not color.decode().isdigit():
                    logger.warning(f"Color data for key {key} not's digit.")
                    continue
                color = int(color.decode())

            canvas.add((int(x), int(y), color))
        return canvas
    except redis.RedisError as e:
        logger.error(f"Error retrieving canvas: {e}")
        raise
    except AttributeError:
        logger.error(f"Error decoding color data from Redis.")
        raise
    except ValueError as e:
        logger.error(e)
        raise

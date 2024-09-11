import redis.client
from django.conf import settings
from core import logger

r = redis.from_url(settings.REDIS_LOCATION)


def save_pixel(x, y, color, pipeline: redis.client.Pipeline = None):
    try:
        key = f"{x}:{y}"
        if pipeline:
            pipeline.hset("pixels", key, color)
        else:
            r.hset("pixels", key, color)
    except redis.RedisError as e:
        logger.error(f"Error saving pixel: {e}")
        raise


def get_pixel(
    x: str | int, y: str | int, pipeline: redis.client.Pipeline | None = None
) -> int | None:
    try:
        key = f"{x}:{y}"
        if pipeline is None:
            color = r.hget("pixels", key)
            if color is None:
                raise ValueError(f"Pixel at ({x}, {y}) not found.")
            if not color.decode().isdigit():
                raise TypeError(f"Color data for key {key} not's digit.")
            return int(color.decode())
        else:
            pipeline.hget("pixels", key)
            return None
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
        pixels = r.hgetall("pixels")

        for key, value in pixels.items():
            x, y = map(int, key.decode().split(":"))
            if value is None:
                logger.warning(f"Color data for key {key} not found.")
                continue
            else:
                if not value.decode().isdigit():
                    logger.warning(f"Color data for key {key} not's digit.")
                    continue
                value = int(value.decode())

            canvas.add((x, y, value))
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


def get_pixel_range(
    x_start: int, x_end: int, y_start, y_end
) -> list[tuple[int, int, str]]:
    fields = [
        f"{x}:{y}" for x in range(x_start, x_end + 1) for y in range(y_start, y_end + 1)
    ]
    values = r.hmget("pixels", fields)
    result = set()
    for field, value in zip(fields, values):
        if value is not None:
            x, y = map(int, field.split(":"))
            num = int(value.decode())
            result.add((x, y, num))
    return result

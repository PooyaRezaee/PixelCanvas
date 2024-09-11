from django.test import TestCase
from unittest.mock import patch
import logging
from core import logger
from ...repositories.redis_operation import (
    save_pixel,
    get_pixel,
    get_canvas,
    get_pixel_range,
)

logger.setLevel(logging.CRITICAL)  # Disable logger


class TestRedisOperations(TestCase):
    @patch("apps.canvas.repositories.redis_operation.r")
    def test_save_pixel(self, mock_redis):
        save_pixel(1, 1, "255")
        mock_redis.hset.assert_called_with("pixels", "1:1", "255")

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_get_pixel(self, mock_redis):
        mock_redis.hget.return_value = b"255"
        color = get_pixel(1, 1)
        self.assertEqual(color, 255)

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_get_pixel_invalid_color(self, mock_redis):
        mock_redis.hget.return_value = b"invalid"
        with self.assertRaises(TypeError):
            get_pixel(1, 1)

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_get_pixel_missing(self, mock_redis):
        mock_redis.hget.return_value = None
        with self.assertRaises(ValueError):
            get_pixel(1, 1)

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_get_canvas(self, mock_redis):
        mock_redis.hgetall.return_value = {b"2:2": b"128", b"1:1": b"255"}

        canvas = get_canvas()
        self.assertEqual(canvas, {(1, 1, 255), (2, 2, 128)})

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_get_range_pixel(self, mock_redis):
        x_start = 4
        x_end = 5
        y_start = 5
        y_end = 6
        values = [b"1", b"2", b"3", b"4"]
        mock_redis.hmget.return_value = values
        result = {(4, 5, 1), (4, 6, 2), (5, 5, 3), (5, 6, 4)}

        canvas = get_pixel_range(x_start, x_end, y_start, y_end)
        self.assertEqual(canvas, result)

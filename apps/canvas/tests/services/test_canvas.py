from django.test import TestCase
from unittest.mock import patch
from ...services.pixel import paint_pixel
from ...enums import Color


class TestServices(TestCase):
    @patch("apps.canvas.repositories.redis_operation.r")
    @patch("apps.canvas.services.pixel.save_pixel")
    def test_paint_pixel_success(self, mock_save_pixel, mock_redis):
        mock_redis.hset.return_value = True
        result = paint_pixel(0, 0, Color.RED)
        self.assertTrue(result)
        mock_save_pixel.assert_called_with(0, 0, Color.RED.value)

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_paint_pixel_invalid_color(self, mock_redis):
        mock_redis.hset.return_value = True
        with self.assertRaises(ValueError):
            paint_pixel(0, 0, "invalid_color")

    @patch("apps.canvas.repositories.redis_operation.r")
    @patch("apps.canvas.services.pixel.save_pixel")
    def test_paint_pixel_failure(self, mock_save_pixel, mock_redis):
        mock_redis.hset.return_value = False
        mock_save_pixel.side_effect = Exception("Error saving pixel")
        result = paint_pixel(0, 0, Color.RED)
        self.assertFalse(result)

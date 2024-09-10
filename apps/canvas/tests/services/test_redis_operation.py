from django.test import TestCase
from unittest.mock import patch,MagicMock
import logging
from core import logger
from ...repositories.redis_operation import save_pixel, get_pixel, get_canvas

logger.setLevel(logging.CRITICAL) # Disable logger


class TestRedisOperations(TestCase):

    @patch('apps.canvas.repositories.redis_operation.r')
    def test_save_pixel(self, mock_redis):
        save_pixel(1, 1, "255")
        mock_redis.set.assert_called_with("pixel:1:1", "255")

    @patch('apps.canvas.repositories.redis_operation.r')
    def test_get_pixel(self, mock_redis):
        mock_redis.get.return_value = b"255"
        color = get_pixel(1, 1)
        self.assertEqual(color, 255)

    @patch('apps.canvas.repositories.redis_operation.r')
    def test_get_pixel_invalid_color(self, mock_redis):
        mock_redis.get.return_value = b"invalid"
        with self.assertRaises(TypeError):
            get_pixel(1, 1)

    @patch('apps.canvas.repositories.redis_operation.r')
    def test_get_pixel_missing(self, mock_redis):
        mock_redis.get.return_value = None
        with self.assertRaises(ValueError):
            get_pixel(1, 1)

    @patch('apps.canvas.repositories.redis_operation.r')
    def test_get_canvas(self, mock_redis):
        mock_redis.keys.return_value = [b"pixel:1:1", b"pixel:2:2"]
        mock_pipeline = MagicMock()
        mock_redis.pipeline.return_value = mock_pipeline
        mock_pipeline.get.side_effect = [b"255", b"128"]
        mock_pipeline.execute.return_value = [b"255", b"128"]

        canvas = get_canvas()
        self.assertEqual(canvas, {(1, 1, 255), (2, 2, 128)})

from django.test import TestCase
from unittest.mock import patch
from ...selectors.pixel import show_canvas, show_part_of_canvas


class TestSelectors(TestCase):
    @patch("apps.canvas.repositories.redis_operation.r")
    def test_show_canvas(self, mock_redis):
        mock_redis.keys.return_value = [b"pixel:1:1", b"pixel:2:2"]
        mock_redis.get.side_effect = [b"255", b"128"]
        canvas = show_canvas()
        self.assertEqual(canvas, [(2, 2, 128), (1, 1, 255)])

    @patch("apps.canvas.repositories.redis_operation.r")
    def test_show_part_of_canvas(self, mock_redis):
        mock_redis.get.side_effect = [b"255", b"128", b"64"]
        result = show_part_of_canvas((1, 1), (2, 2))
        self.assertEqual(set(result), {(1, 1, 255), (1, 2, 128), (2, 1, 64)})

    def test_show_part_of_canvas_invalid_range(self):
        with self.assertRaises(ValueError):
            show_part_of_canvas((2, 2), (1, 1))

from django.test import TestCase
from unittest.mock import patch, MagicMock
from ...selectors.pixel import show_canvas, show_part_of_canvas


class TestSelectors(TestCase):
    @patch("apps.canvas.repositories.redis_operation.r")
    def test_show_canvas(self, mock_redis):
        mock_pipeline = MagicMock()
        mock_redis.pipeline.return_value = mock_pipeline
        mock_pipeline.get.side_effect = [b"255", b"128"]
        mock_pipeline.execute.return_value = [b"255", b"128"]
        mock_redis.keys.return_value = [b"pixel:1:1", b"pixel:2:2"]

        canvas = show_canvas()
        self.assertEqual(canvas, [(2, 2, 128), (1, 1, 255)])

    @patch("apps.canvas.selectors.pixel.r")
    def test_show_part_of_canvas(self, mock_redis):
        mock_pipeline = MagicMock()
        mock_redis.pipeline.return_value = mock_pipeline

        fake_data = [str(i).encode() for i in range(1, 10)]
        mock_pipeline.get.side_effect = fake_data
        mock_pipeline.execute.return_value = fake_data

        fake_result = []
        color_index = 0
        for x in range(2, 5):
            for y in range(2, 5):
                fake_result.append((x, y, int(fake_data[color_index].decode())))
                color_index += 1

        result = show_part_of_canvas((2, 4), (2, 4))
        self.assertEqual(len(result), 9)
        self.assertEqual(set(result), set(fake_result))

    def test_show_part_of_canvas_invalid_range(self):
        with self.assertRaises(ValueError):
            show_part_of_canvas((3, 2), (2, 1))

from django.test import TestCase
from unittest.mock import patch
from ...selectors.pixel import show_canvas, show_pixel_range


class TestSelectors(TestCase):
    @patch("apps.canvas.selectors.pixel.get_canvas")
    def test_show_canvas(self, mock_get_canvas):
        mock_get_canvas.return_value = {(2,2,128),(1,1,255)}

        canvas = show_canvas()
        self.assertEqual(canvas, [(2, 2, 128), (1, 1, 255)])

    @patch("apps.canvas.selectors.pixel.get_pixel_range")
    def test_show_pixel_range(self, mock_get_pixel_range):
        fake_data = [str(i).encode() for i in range(1, 10)]
        fake_result = set()
        color_index = 0
        for x in range(2, 5):
            for y in range(2, 5):
                fake_result.add((x, y, int(fake_data[color_index].decode())))
                color_index += 1

        mock_get_pixel_range.return_value = fake_result

        result = show_pixel_range((2, 4), (2, 4))
        self.assertEqual(len(result), 9)
        self.assertEqual(set(result), set(fake_result))

    def test_show_part_of_canvas_invalid_range(self):
        with self.assertRaises(ValueError):
            show_pixel_range((3, 2), (2, 1))

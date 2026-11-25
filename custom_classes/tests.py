from django.test import SimpleTestCase
from .rectangle import Rectangle

class RectangleTests(SimpleTestCase):
    def test_iteration_order_and_values(self):
        rectangle = Rectangle(10, 5)
        self.assertEqual(
            list(rectangle),
            [{"length": 10}, {"width": 5}]
        )

    def test_length_and_width_are_integers(self):
        with self.assertRaises(TypeError):
            Rectangle("10", 5)

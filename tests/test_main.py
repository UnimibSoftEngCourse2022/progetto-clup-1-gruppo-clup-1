import unittest

from src.clup.main import add_two


class TestMain(unittest.TestCase):
    def test_add_two_1(self):
        result = add_two(3)
        self.assertEqual(result, 5)

    def test_add_two_2(self):
        result = add_two(4)
        self.assertEqual(result, 6)

    def test_add_two_3(self):
        result = add_two(6)
        self.assertEqual(result, 8)


if __name__ == '__main__':
    unittest.main()


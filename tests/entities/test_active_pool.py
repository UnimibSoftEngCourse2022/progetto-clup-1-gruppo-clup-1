import unittest

from src.clup.entities.active_pool import ActivePool


class TestActivePool(unittest.TestCase):
    def setUp(self):
        self.ap = ActivePool()

    def test_active_pool_is_empty_after_init(self):
        self.assertTrue(len(self.ap) == 0)

    def test_add_increments_length(self):
        self.ap.add('a')

        self.assertTrue(len(self.ap) == 1)

    def test_added_elements_are_in_pool(self):
        self.ap.add('a')
        self.ap.add('b')

        self.assertTrue('a' in self.ap)
        self.assertTrue('b' in self.ap)
        self.assertFalse('c' in self.ap)

    def test_after_remove_element_is_not_in_pool(self):
        self.ap.add('a')

        self.ap.remove('a')

        self.assertTrue('a' not in self.ap)

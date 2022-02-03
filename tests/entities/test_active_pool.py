import unittest
from collections.abc import Iterable

from src.clup.entities.exceptions \
    import MaxCapacityReachedError, EmptyPoolError
from src.clup.entities.active_pool import ActivePool


class TestActivePool(unittest.TestCase):
    def setUp(self):
        self.ap = ActivePool(capacity=10)

    def test_is_empty_after_init(self):
        ap = ActivePool()

        self.assertTrue(len(ap) == 0)
        self.assertEqual(ap.capacity, 0)
        self.assertEqual(ap.current_quantity, 0)

    def test_capacity_is_passed_in_init(self):
        ap = ActivePool(capacity=10)

        self.assertTrue(len(ap) == 0)
        self.assertEqual(ap.capacity, 10)

    def test_capacity_is_settable(self):
        self.ap.capacity = 5

        self.assertEqual(self.ap.capacity, 5)

    def test_capacity_is_settable_if_no_elements_are_discarded(self):
        self.ap.add('a')
        self.ap.add('b')

        self.ap.capacity = 15

        self.assertEqual(self.ap.capacity, 15)

    def test_capacity_is_not_set_negative(self):
        with self.assertRaises(ValueError):
            self.ap.capacity = -1

    def test_capacity_is_not_set_less_than_total_elements(self):
        ap = ActivePool(capacity=10)
        ap.add('a')
        ap.add('b')

        with self.assertRaises(ValueError):
            ap.capacity = 1

    def test_add_increments_length(self):
        self.ap.add('a')

        self.assertTrue(len(self.ap) == 1)

    def test_add_throws_if_max_capacity_is_reached(self):
        ap = ActivePool(capacity=1)
        ap.add('a')
        ap.consume('a')

        with self.assertRaises(MaxCapacityReachedError):
            ap.add('b')

    def test_add_throws_if_active_elements_fill_remaining_capacity(self):
        ap = ActivePool(capacity=1)
        ap.add('a')

        with self.assertRaises(MaxCapacityReachedError):
            ap.add('b')

    def test_added_elements_are_in_pool(self):
        self.ap.add('a')
        self.ap.add('b')

        self.assertTrue('a' in self.ap)
        self.assertTrue('b' in self.ap)
        self.assertFalse('c' in self.ap)

    def test_after_invalidate_element_is_not_in_pool(self):
        self.ap.add('a')

        self.ap.invalidate('a')

        self.assertTrue('a' not in self.ap)

    def test_invalidate_throws_if_element_is_not_in_pool(self):
        with self.assertRaises(ValueError):
            self.ap.invalidate('z')

    def test_active_pool_is_iterable(self):
        is_iterable = isinstance(self.ap, Iterable)

        self.assertTrue(is_iterable)

    def test_active_pool_iterator_return_elements(self):
        elements = set()
        self.ap.add('a')
        self.ap.add('b')

        for e in self.ap:
            elements.add(e)

        self.assertEqual(elements, {'a', 'b'})

    def test_consume_increments_current_quantity(self):
        self.ap.add('a')
        quantity = self.ap.current_quantity

        self.ap.consume('a')

        self.assertEqual(self.ap.current_quantity, quantity + 1)

    def test_consume_removes_element_from_active_pool(self):
        self.ap.add('a')

        self.ap.consume('a')

        self.assertTrue('a' not in self.ap)

    def test_consume_throws_if_element_not_in_pool(self):
        with self.assertRaises(ValueError):
            self.ap.consume('z')

    def test_free_decrements_current_quantity(self):
        self.ap.add('a')
        self.ap.consume('a')
        quantity = self.ap.current_quantity

        self.ap.free()

        self.assertEqual(self.ap.current_quantity, quantity - 1)

    def test_free_throws_if_current_quantity_becomes_negative(self):
        with self.assertRaises(EmptyPoolError):
            self.ap.free()

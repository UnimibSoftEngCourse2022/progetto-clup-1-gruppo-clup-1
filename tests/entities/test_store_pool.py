import unittest
from unittest.mock import Mock

from src.clup.entities.store_pool import StorePool


class TestStorePool(unittest.TestCase):
    def setUp(self):
        self.sap = StorePool()

    def test_is_empty_after_init(self):
        self.assertEqual(len(self.sap.enabled), 0)
        self.assertEqual(len(self.sap.to_free), 0)

    def test_add_increments_length(self):
        self.sap.add('a')

        self.assertTrue(len(self.sap.enabled) == 1)

    def test_added_elements_are_in_pool(self):
        self.sap.add('a')
        self.sap.add('b')

        self.assertTrue('a' in self.sap.enabled)
        self.assertTrue('b' in self.sap.enabled)
        self.assertTrue('c' not in self.sap.enabled)

    def test_last_added_is_none_after_init(self):
        self.assertEqual(self.sap.last_added, None)

    def test_add_save_element_in_class_field(self):
        self.sap.add('a')
        self.assertEqual(self.sap.last_added, 'a')

        self.sap.add('b')
        self.assertEqual(self.sap.last_added, 'b')

    def test_consume_moves_element_from_pool_to_to_free(self):
        reservation_id = 1
        self.sap.add(reservation_id)

        self.sap.consume(reservation_id)

        self.assertTrue(reservation_id not in self.sap.enabled)
        self.assertTrue(reservation_id in self.sap.to_free)

    def test_consume_throws_on_unexistent_element(self):
        with self.assertRaises(ValueError):
            self.sap.consume(-1)

    def test_free_removes_element_from_to_free(self):
        self.sap.to_free.append('a')

        self.sap.free('a')

        self.assertTrue('a' not in self.sap.to_free)

    def test_free_throws_on_unexistent_element(self):
        with self.assertRaises(ValueError):
            self.sap.free(-1)

    def test_get_to_free_containes_same_element_of_to_free_container(self):
        self.sap.to_free.append('a')
        self.sap.to_free.append('b')

        to_free = self.sap.get_to_free()

        self.assertTrue('a' in to_free)
        self.assertTrue('b' in to_free)

    def test_get_to_free_returns_independent_object(self):
        self.sap.to_free.append('a')
        self.sap.to_free.append('b')

        to_free = self.sap.get_to_free()
        self.sap.to_free.append('c')

        self.assertTrue('a' in to_free)
        self.assertTrue('b' in to_free)
        self.assertTrue('c' not in to_free)


class TestStorePoolAsObject(unittest.TestCase):
    def setUp(self):
        self.sp = StorePool()

    def test_empty_observers_by_default(self):
        self.assertEqual(len(self.sp._observers), 0)

    def test_attach_adds_the_element_to_observers(self):
        self.sp.attach('observer')

        self.assertTrue('observer' in self.sp._observers)

    def test_detach_removes_the_element_from_observers(self):
        self.sp._observers.append('observer')

        self.sp.detach('observer')

        self.assertTrue('observer' not in self.sp._observers)

    def test_notify_calls_update_on_observers(self):
        mock_observer_1 = Mock()
        mock_observer_2 = Mock()
        self.sp._observers.append(mock_observer_1)
        self.sp._observers.append(mock_observer_2)

        self.sp.notify()

        mock_observer_1.update.assert_called_once_with(self.sp)
        mock_observer_2.update.assert_called_once_with(self.sp)

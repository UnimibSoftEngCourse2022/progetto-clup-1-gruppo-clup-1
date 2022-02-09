import unittest

from src.clup.entities.store_active_pool import StoreActivePool


class TestStoreActivePool(unittest.TestCase):
    def setUp(self):
        self.sap = StoreActivePool()

    def test_is_empty_after_init(self):
        self.assertEqual(len(self.sap.pool), 0)
        self.assertEqual(len(self.sap.to_free), 0)

    def test_add_increments_length(self):
        self.sap.add('a')

        self.assertTrue(len(self.sap.pool) == 1)

    def test_added_elements_are_in_pool(self):
        self.sap.add('a')
        self.sap.add('b')

        self.assertTrue('a' in self.sap.pool)
        self.assertTrue('b' in self.sap.pool)
        self.assertTrue('c' not in self.sap.pool)

    def test_consume_moves_element_from_pool_to_to_free(self):
        reservation_id = 1
        self.sap.add(reservation_id)

        self.sap.consume(reservation_id)

        self.assertTrue(reservation_id not in self.sap.pool)
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

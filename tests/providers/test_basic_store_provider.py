import unittest

from src.clup.entities.store import Store
from src.clup.providers.basic.basic_store_provider import BasicStoreProvider


class TestBasicStoreProvider(unittest.TestCase):
    def setUp(self):
        self.bsp = BasicStoreProvider()
        self.store1 = Store(1, None, None)
        self.store2 = Store(2, None, None)

    def test_is_empty_after_initialization(self):
        stores = self.bsp.get_stores()
        is_empty = len(stores) == 0

        self.assertTrue(is_empty)

    def test_element_is_added(self):
        self.bsp.add_store(self.store1)
        stores = self.bsp.get_stores()

        self.assertTrue(self.store1 in stores)

    def test_only_corrects_elements_added(self):
        self.bsp.add_store(self.store1)
        self.bsp.add_store(self.store2)
        stores = self.bsp.get_stores()

        self.assertTrue(len(stores) == 2)

    def test_add_stores_with_same_id_throws(self):
        store1 = Store(1, 2, 3)
        store2 = Store(1, 5, 6)

        self.bsp.add_store(store1)

        with self.assertRaises(ValueError):
            self.bsp.add_store(store2)

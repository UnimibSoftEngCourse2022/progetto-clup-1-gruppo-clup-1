import unittest

from src.clup.entities.store import Store
from src.clup.providers.basic_store_provider import BasicStoreProvider


class TestBasicStoreProvider(unittest.TestCase):
    def setUp(self):
        self.bsp = BasicStoreProvider()
        self.store1 = Store(1, None, None, None)
        self.store2 = Store(2, None, None, None)

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

    def test_add_store_twice_throws(self):
        self.bsp.add_store(self.store1)

        with self.assertRaises(ValueError):
            self.bsp.add_store(self.store1)
    

class TestQueuesOfBasicStoreProvider(unittest.TestCase):
    def setUp(self):
        self.bsp = BasicStoreProvider()
        self.store1 = Store(1, None, None, None)
        self.store2 = Store(2, None, None, None)

    def test_queue_of_new_store_is_empty(self):
        store_id = 1
        self.bsp.add_store(self.store1)

        store_queue = self.bsp.get_queue(self.store1.id)
        is_empty = len(store_queue) == 0

        self.assertTrue(is_empty)

    def test_add_element_to_queue(self):
        self.bsp.add_store(self.store1)

        reservation = (1, 2, 3)
        self.bsp.add_to_queue(self.store1.id, reservation)
        queue = self.bsp.get_queue(self.store1.id)

        self.assertTrue(reservation in queue)

    def test_different_queues_for_different_stores(self):
        self.bsp.add_store(self.store1)
        self.bsp.add_store(self.store2)
        reservation1 = (1, 2, 3)
        reservation2 = (4, 5, 6)
        
        self.bsp.add_to_queue(self.store1.id, reservation1)
        self.bsp.add_to_queue(self.store2.id, reservation2)
        queue1 = self.bsp.get_queue(self.store1.id)
        queue2 = self.bsp.get_queue(self.store2.id)

        self.assertTrue(reservation1 in queue1)
        self.assertTrue(reservation2 in queue2)
        self.assertNotEqual(queue1, queue2)

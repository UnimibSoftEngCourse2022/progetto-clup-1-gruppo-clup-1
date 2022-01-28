import unittest
from src.clup.providers.basic_store_provider import BasicStoreProvider

class TestBasicStoreProvider(unittest.TestCase):
    
    def test_is_empty_after_initialization(self):
        bsp = BasicStoreProvider()

        stores = bsp.get_stores()
        is_empty = len(stores) == 0

        self.assertTrue(is_empty)
    
    def test_correct_element_added(self):
        bsp = BasicStoreProvider()
        store_id = 1

        bsp.add_store(store_id)
        stores = bsp.get_stores()
        is_id_in_stores = store_id in stores

        self.assertTrue(is_id_in_stores)

    def test_only_corrects_elements_added(self):
        bsp = BasicStoreProvider()
        store1_id = 1
        store2_id = 2

        bsp.add_store(store1_id)
        bsp.add_store(store2_id)
        stores = bsp.get_stores()
        is_correct_length = len(stores) == 2

        self.assertTrue(is_correct_length)

    def test_add_store_twice_froze(self):
        bsp = BasicStoreProvider()
        store_id = 1

        bsp.add_store(store_id)
        with self.assertRaises(ValueError):
            bsp.add_store(store_id)
    
class TestQueuesOfBasicStoreProvider(unittest.TestCase):

    def test_queue_of_new_store_is_empty(self):
        bsp = BasicStoreProvider()
        store_id = 1
        bsp.add_store(store_id)

        store_queue = bsp.get_queue(store_id)
        is_empty = len(store_queue) == 0

        self.assertTrue(is_empty)

    def test_set_a_new_queue(self):
        bsp = BasicStoreProvider()
        store_id = 1
        bsp.add_store(store_id)

        new_queue = [1]
        bsp.set_queue(store_id, new_queue)
        queue = bsp.get_queue(store_id)

        self.assertEqual(new_queue, queue)

    def test_different_queues_for_different_stores(self):
        bsp = BasicStoreProvider()
        store1_id = 1
        store2_id = 3
        bsp.add_store(store1_id)
        bsp.add_store(store2_id)
        new_queue1 = [1]
        new_queue2 = [2]
        
        bsp.set_queue(store1_id, new_queue1)
        bsp.set_queue(store2_id, new_queue2)
        queue1 = bsp.get_queue(store1_id)
        queue2 = bsp.get_queue(store2_id)

        self.assertNotEqual(queue1, queue2)

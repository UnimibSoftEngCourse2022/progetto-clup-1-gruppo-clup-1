import unittest

from src.clup.providers.basic_queue_provider import BasicQueueProvider


class TestBasicQueueProvider(unittest.TestCase):
    def setUp(self):
        self.bqp = BasicQueueProvider()

    @unittest.skip('incomplete')
    def test_unexistent_store_id_gets_empty_queue_and_pool(self):
        store_id = 1
        queue = self.bqp.get_waiting_queue(store_id)
        pool = self.bqp.get_active_pool(store_id)

        self.assertEqual(len(queue), 0)
        self.assertEqual(len(pool), 0)

    @unittest.skip('incomplete')
    def test_modifications_on_store_queues_are_presisted(self):
        store_id = 1
        queue = self.bqp.get_waiting_queue(store_id)
        pool = self.bqp.get_active_pool(store_id)

        queue.push('a')
        pool.capacity = 10
        pool.add('b')

        self.assertTrue('a' in self.bqp.get_waiting_queue(store_id))
        self.assertTrue('b' in self.bqp.get_active_pool(store_id))
        self.assertEqual(self.bqp.get_active_pool(store_id).capacity, 10)

    @unittest.skip('incomplete')
    def test_modifications_on_different_stores_act_on_different_queues(self):
        store1_id = 1
        store2_id = 2
        queue1 = self.bqp.get_waiting_queue(store1_id)
        pool1 = self.bqp.get_active_pool(store1_id)
        queue2 = self.bqp.get_waiting_queue(store2_id)
        pool2 = self.bqp.get_active_pool(store2_id)

        pool1.capacity = 5
        pool2.capacity = 9
        queue1.push('a')
        queue2.push('b')
        pool1.add('c')
        pool2.add('d')

        self.assertTrue('a' not in self.bqp.get_waiting_queue(store2_id))
        self.assertTrue('b' not in self.bqp.get_waiting_queue(store1_id))
        self.assertTrue('c' not in self.bqp.get_active_pool(store2_id))
        self.assertTrue('d' not in self.bqp.get_active_pool(store1_id))
        self.assertNotEqual(pool1.capacity, pool2.capacity)

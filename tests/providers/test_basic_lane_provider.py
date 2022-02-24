import unittest

from src.clup.providers.basic.basic_lane_provider import BasicLaneProvider


class TestBasicLaneProvider(unittest.TestCase):
    def setUp(self):
        self.bqp = BasicLaneProvider()

    def test_by_default_gets_empty_queue_and_pools(self):
        store_id = 1
        aisle_id = 10
        queue = self.bqp.get_waiting_queue(aisle_id)
        pool = self.bqp.get_aisle_pool(aisle_id)
        store_pool = self.bqp.get_store_pool(store_id)

        self.assertEqual(len(queue), 0)
        self.assertEqual(len(pool), 0)
        self.assertEqual(len(store_pool.enabled), 0)
        self.assertEqual(len(store_pool.to_free), 0)

    def test_modifications_on_store_queues_are_persistent(self):
        aisle_id = 1
        queue = self.bqp.get_waiting_queue(aisle_id)
        pool = self.bqp.get_aisle_pool(aisle_id)
        store_id = 10
        store_pool = self.bqp.get_store_pool(store_id)

        queue.push('a')
        pool.capacity = 10
        pool.add('b')
        store_pool.add('c')

        self.assertTrue('a' in self.bqp.get_waiting_queue(aisle_id))
        self.assertTrue('b' in self.bqp.get_aisle_pool(aisle_id))
        self.assertEqual(self.bqp.get_aisle_pool(aisle_id).capacity, 10)
        self.assertTrue('c' in self.bqp.get_store_pool(store_id).enabled)

    def test_modifications_on_different_stores_act_on_different_queues(self):
        aisle1_id = 1
        aisle2_id = 2
        queue1 = self.bqp.get_waiting_queue(aisle1_id)
        pool1 = self.bqp.get_aisle_pool(aisle1_id)
        queue2 = self.bqp.get_waiting_queue(aisle2_id)
        pool2 = self.bqp.get_aisle_pool(aisle2_id)
        store1_id = 10
        store2_id = 20
        store1_pool = self.bqp.get_store_pool(store1_id)
        store2_pool = self.bqp.get_store_pool(store2_id)

        pool1.capacity = 5
        pool2.capacity = 9
        queue1.push('a')
        queue2.push('b')
        pool1.add('c')
        pool2.add('d')
        store1_pool.add('e')
        store2_pool.add('f')

        self.assertTrue('a' not in self.bqp.get_waiting_queue(aisle2_id))
        self.assertTrue('b' not in self.bqp.get_waiting_queue(aisle1_id))
        self.assertTrue('c' not in self.bqp.get_aisle_pool(aisle2_id))
        self.assertTrue('d' not in self.bqp.get_aisle_pool(aisle1_id))
        self.assertNotEqual(pool1.capacity, pool2.capacity)
        self.assertTrue('e' not in self.bqp.get_store_pool(store2_id).enabled)
        self.assertTrue('f' not in self.bqp.get_store_pool(store1_id).enabled)

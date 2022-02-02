import unittest
from collections import defaultdict

from src.clup.entities.exceptions import EmptyPoolError
from src.clup.entities.active_pool import ActivePool
from src.clup.entities.waiting_queue import WaitingQueue
from src.clup.providers.queue_provider_abc import QueueProvider
from src.clup.usecases.free_reservation_usecase import FreeReservationUseCase


class MockQueueProvider(QueueProvider):
    def __init__(self):
        self.pools = defaultdict(ActivePool)
        self.queues = defaultdict(WaitingQueue)

    def get_waiting_queue(self, store_id):
        return self.queues[store_id]

    def get_active_pool(self, store_id):
        return self.pools[store_id]


class TestFreeReservationUseCase(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockQueueProvider()
        self.u = FreeReservationUseCase(self.queue_provider)

    def test_pool_current_quantity_is_decremented(self):
        store_id = 1
        pool = self.queue_provider.get_active_pool(store_id)
        pool.capacity = 5
        pool.add('a')
        pool.consume('a')
        queue = self.queue_provider.get_waiting_queue(store_id)
        queue.push('a')
        quantity = pool.current_quantity

        self.u.execute(store_id)

        self.assertEqual(pool.current_quantity, quantity-1)

    def test_emptypoolerror_is_forwarded(self):
        store_id = 1

        with self.assertRaises(EmptyPoolError):
            self.u.execute(store_id)

    def test_first_element_in_queue_is_popped_into_pool(self):
        store_id = 1
        pool = self.queue_provider.get_active_pool(store_id)
        pool.capacity = 5
        pool.add('a')
        pool.consume('a')
        queue = self.queue_provider.get_waiting_queue(store_id)
        queue.push('a')
        queue.push('b')

        self.u.execute(store_id)

        self.assertTrue('a' in pool)
        self.assertTrue('b' in queue)

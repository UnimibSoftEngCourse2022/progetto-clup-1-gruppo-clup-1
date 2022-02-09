import unittest

from src.clup.entities.exceptions import EmptyPoolError
from src.clup.usecases.free_reservation_usecase import FreeReservationUseCase
from tests.usecases.mock_queue_provider import MockQueueProvider


class TestFreeReservationUseCase(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockQueueProvider()
        self.u = FreeReservationUseCase(self.queue_provider)

    def test_pool_current_quantity_is_decremented(self):
        store_id = 1
        pool = self.queue_provider.get_aisle_pool(store_id)
        pool.capacity = 5
        pool.add('a')
        pool.consume('a')
        queue = self.queue_provider.get_waiting_queue(store_id)
        queue.push('a')
        quantity = pool.current_quantity

        self.u.execute(store_id)

        self.assertEqual(pool.current_quantity, quantity - 1)

    def test_emptypoolerror_is_forwarded(self):
        store_id = 1

        with self.assertRaises(EmptyPoolError):
            self.u.execute(store_id)

    def test_first_element_in_queue_is_popped_into_pool(self):
        store_id = 1
        pool = self.queue_provider.get_aisle_pool(store_id)
        pool.capacity = 5
        pool.add('a')
        pool.consume('a')
        queue = self.queue_provider.get_waiting_queue(store_id)
        queue.push('a')
        queue.push('b')

        self.u.execute(store_id)

        self.assertTrue('a' in pool)
        self.assertTrue('b' in queue)

    def test_pool_is_unchanged_if_queue_is_empty(self):
        store_id = 1
        pool = self.queue_provider.get_aisle_pool(store_id)
        pool.capacity = 5
        pool.add('a')
        pool.consume('a')

        self.u.execute(store_id)

        self.assertEqual(len(pool), 0)

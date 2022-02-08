import unittest

from tests.usecases.mock_queue_provider import MockQueueProvider

from src.clup.entities.active_pool import ActivePool
from src.clup.entities.exceptions \
    import MaxCapacityReachedError, EmptyQueueError
from src.clup.entities.waiting_queue import WaitingQueue
from src.clup.providers.queue_provider_abc import QueueProvider
from src.clup.usecases.enable_reservation_usecase \
    import EnableReservationUseCase


class TestEnableReservationUseCase(unittest.TestCase):
    def setUp(self):
        store_id = 1
        self.queue_provider = MockQueueProvider()
        self.queue_provider.get_active_pool(store_id).capacity = 5
        self.u = EnableReservationUseCase(self.queue_provider)

    def test_enable_takes_element_from_queue_and_add_to_pool(self):
        store_id = 1
        self.queue_provider.get_waiting_queue(store_id).push('a')

        self.u.execute(store_id, 'a')

        self.assertTrue('a' in self.queue_provider.get_active_pool(store_id))

    def test_takes_element_in_arbitrary_position_and_add_to_pool(self):
        store_id = 1
        self.queue_provider.get_waiting_queue(store_id).push('a')
        self.queue_provider.get_waiting_queue(store_id).push('b')
        self.queue_provider.get_waiting_queue(store_id).push('c')

        self.u.execute(store_id, 'b')

        self.assertTrue('b' in self.queue_provider.get_active_pool(store_id))

    def test_enable_on_empty_queue_throws(self):
        store_id = 1

        with self.assertRaises(EmptyQueueError):
            self.u.execute(store_id, 'a')

    def test_throws_if_element_is_not_in_waiting_queue(self):
        store_id = 1
        self.queue_provider.get_waiting_queue(store_id).push('a')

        with self.assertRaises(ValueError):
            self.u.execute(store_id, 'z')

    def test_enable_on_full_active_pool_throws(self):
        store_id = 1
        self.queue_provider.get_active_pool(store_id).capacity = 1
        self.queue_provider.get_waiting_queue(store_id).push('a')
        self.queue_provider.get_waiting_queue(store_id).push('b')
        self.u.execute(store_id, 'b')

        with self.assertRaises(MaxCapacityReachedError):
            self.u.execute(store_id, 'a')

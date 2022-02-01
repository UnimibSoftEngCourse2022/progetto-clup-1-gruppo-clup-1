import unittest
from collections import defaultdict

from src.clup.entities.waiting_queue import WaitingQueue
from src.clup.providers.queue_provider_abc import QueueProvider
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase


class MockQueueProvider(QueueProvider):
    def __init__(self):
        self.queues = defaultdict(WaitingQueue)

    def get_waiting_queue(self, store_id):
        return self.queues[store_id]

    def get_active_pool(self, store_id):
        raise NotImplementedError


class MockReservationProvider:
    def __init__(self, throws_on_add=False):
        self.reservations = []
        self.throws_on_add = throws_on_add

    def get_reservations(self):
        return self.reservations

    def add_reservation(self, reservation):
        if(self.throws_on_add):
            raise ValueError()
        self.reservations.append(reservation)


class TestMakeReservationUseCase(unittest.TestCase):
    def setUp(self):
        self.store1_id = 1
        self.store2_id = 2
        self.user1_id = 11
        self.user2_id = 22
        self.queue_provider = MockQueueProvider()
        self.reservation_provider = MockReservationProvider()
        self.u = MakeReservationUseCase(
            self.queue_provider, self.reservation_provider)

    def test_reservation_contains_store_and_user_id(self):
        reservation = self.u.execute(self.store1_id, self.user1_id)

        self.assertEqual(reservation.store_id, self.store1_id)
        self.assertEqual(reservation.user_id, self.user1_id)

    def test_reservations_are_stored_in_reservation_provider(self):
        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store2_id, self.user2_id)
        reservations = self.reservation_provider.get_reservations()

        self.assertTrue(r1 in reservations)
        self.assertTrue(r2 in reservations)

    def test_reservation_should_be_in_the_queue_of_the_store(self):
        r = self.u.execute(self.store1_id, self.user1_id)
        waiting_queue = self.queue_provider.get_waiting_queue(self.store1_id)
        is_id_in_queue = r in waiting_queue

        self.assertTrue(is_id_in_queue)

    def test_reservations_should_have_different_ids(self):
        reservation1 = self.u.execute(self.store1_id, self.user1_id)
        reservation2 = self.u.execute(self.store1_id, self.user1_id)

        self.assertNotEqual(reservation1.id, reservation2.id)

    def test_reservations_in_different_stores_should_be_in_their_queue(self):
        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store2_id, self.user1_id)
        waiting_queue1 = self.queue_provider.get_waiting_queue(self.store1_id)
        waiting_queue2 = self.queue_provider.get_waiting_queue(self.store2_id)
        is_id1_in_queue1 = r1 in waiting_queue1
        is_id2_in_queue2 = r2 in waiting_queue2

        self.assertTrue(is_id1_in_queue1)
        self.assertTrue(is_id2_in_queue2)

    def test_reservations_from_different_users_should_be_in_same_queue(self):
        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store1_id, self.user2_id)
        waiting_queue = self.queue_provider.get_waiting_queue(self.store1_id)
        is_id1_in_queue = r1 in waiting_queue
        is_id2_in_queue = r2 in waiting_queue

        self.assertTrue(is_id1_in_queue)
        self.assertTrue(is_id2_in_queue)

    def test_should_throw_if_add_reservation_throws(self):
        reservation_provider = MockReservationProvider(throws_on_add=True)
        u = MakeReservationUseCase(self.queue_provider, reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)

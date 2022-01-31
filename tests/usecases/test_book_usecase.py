import unittest
from collections import defaultdict

from src.clup.usecases.book_usecase import BookUseCase


class MockQueueProvider:
    def __init__(self, throws_on_add=False):
        self.queues = defaultdict(tuple)
        self.throws_on_add = throws_on_add

    def add_to_queue(self, store_id, element):
        if(self.throws_on_add):
            raise ValueError()
        self.queues[store_id] = self.queues[store_id] + (element, )


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


class TestBookUsecase(unittest.TestCase):
    def setUp(self):
        self.store1_id = 1
        self.store2_id = 2
        self.user1_id = 11
        self.user2_id = 22
        self.queue_provider = MockQueueProvider()
        self.reservation_provider = MockReservationProvider()
        self.u = BookUseCase(self.queue_provider, self.reservation_provider)

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
        is_id_in_queue = r.id in self.queue_provider.queues[self.store1_id]

        self.assertTrue(is_id_in_queue)

    def test_reservations_should_have_different_ids(self):
        reservation1 = self.u.execute(self.store1_id, self.user1_id)
        reservation2 = self.u.execute(self.store1_id, self.user1_id)

        self.assertNotEqual(reservation1.id, reservation2.id)

    def test_reservations_in_different_stores_should_be_in_their_queue(self):
        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store2_id, self.user1_id)
        is_id1_in_queue1 = r1.id in self.queue_provider.queues[self.store1_id]
        is_id2_in_queue2 = r2.id in self.queue_provider.queues[self.store2_id]

        self.assertTrue(is_id1_in_queue1)
        self.assertTrue(is_id2_in_queue2)

    def test_reservations_from_different_users_should_be_in_same_queue(self):
        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store1_id, self.user2_id)
        is_id1_in_queue = r1.id in self.queue_provider.queues[self.store1_id]
        is_id2_in_queue = r2.id in self.queue_provider.queues[self.store1_id]

        self.assertTrue(is_id1_in_queue)
        self.assertTrue(is_id2_in_queue)

    def test_should_throw_if_set_queue_throws(self):
        queue_provider = MockQueueProvider(throws_on_add=True)
        u = BookUseCase(queue_provider, self.reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)

    def test_should_throw_if_add_reservation_throws(self):
        reservation_provider = MockReservationProvider(throws_on_add=True)
        u = BookUseCase(self.queue_provider, reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)

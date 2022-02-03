import unittest

from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase

from tests.usecases.mock_queue_provider import MockQueueProvider


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

    def test_reservations_should_have_different_ids(self):
        reservation1 = self.u.execute(self.store1_id, self.user1_id)
        reservation2 = self.u.execute(self.store1_id, self.user1_id)

        self.assertNotEqual(reservation1.id, reservation2.id)

    def test_reservation_id_should_be_in_pool_if_pool_is_not_full(self):
        self.queue_provider.get_active_pool(self.store1_id).capacity = 1

        r = self.u.execute(self.store1_id, self.user1_id)
        pool = self.queue_provider.get_active_pool(self.store1_id)
        queue = self.queue_provider.get_waiting_queue(self.store1_id)

        self.assertTrue(r.id in pool)
        self.assertTrue(r.id not in queue)

    def test_reservation_id_should_be_in_queue_if_pool_is_full(self):
        self.queue_provider.get_active_pool(self.store1_id).capacity = 0

        r = self.u.execute(self.store1_id, self.user1_id)
        pool = self.queue_provider.get_active_pool(self.store1_id)
        queue = self.queue_provider.get_waiting_queue(self.store1_id)

        self.assertTrue(r.id in queue)
        self.assertTrue(r.id not in pool)

    def test_reservation_id_should_be_in_queue_after_pool_is_filled(self):
        self.queue_provider.get_active_pool(self.store1_id).capacity = 1

        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store1_id, self.user2_id)
        pool = self.queue_provider.get_active_pool(self.store1_id)
        queue = self.queue_provider.get_waiting_queue(self.store1_id)

        self.assertTrue(r1.id in pool)
        self.assertTrue(r2.id in queue)

    def test_different_users_reservations_should_be_in_same_queue(self):
        r1 = self.u.execute(self.store1_id, self.user1_id)
        r2 = self.u.execute(self.store1_id, self.user2_id)
        queue = self.queue_provider.get_waiting_queue(self.store1_id)

        self.assertTrue(r1.id in queue)
        self.assertTrue(r2.id in queue)

    def test_should_throw_if_add_reservation_throws(self):
        reservation_provider = MockReservationProvider(throws_on_add=True)
        u = MakeReservationUseCase(self.queue_provider, reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)

import unittest

from src.clup.usecases.book_usecase import BookUseCase


class MockStoreProvider:
    def __init__(self, throws_on_set=False, throws_on_get=False):
        self.queue = ()
        self.throws_on_set = throws_on_set
        self.throws_on_get = throws_on_get

    def set_queue(self, store_id, queue):
        if(self.throws_on_set):
            raise ValueError()
        self.queue = queue

    def get_queue(self, store_id):
        if(self.throws_on_get):
            raise ValueError()
        return self.queue


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
        self.store_provider = MockStoreProvider()
        self.reservation_provider = MockReservationProvider()
        self.usecase = BookUseCase(self.store_provider, self.reservation_provider)

    def test_reservation_contains_store_and_user_id(self):
        reservation = self.usecase.execute(self.store1_id, self.user1_id)
        _, r_store_id, r_user_id = reservation

        self.assertEqual(r_store_id, self.store1_id)
        self.assertEqual(r_user_id, self.user1_id)

    def test_reservations_are_stored_in_reservation_provider(self):
        r1 = self.usecase.execute(self.store1_id, self.user1_id)
        r2 = self.usecase.execute(self.store2_id, self.user2_id)
        reservations = self.reservation_provider.get_reservations()

        self.assertTrue(r1 in reservations)
        self.assertTrue(r2 in reservations)
        

    def test_reservation_should_be_in_the_queue_of_the_store(self):
        r_id, _, _ = self.usecase.execute(self.store1_id, self.user1_id)
        is_id_in_queue = r_id in self.store_provider.get_queue(self.store1_id)

        self.assertTrue(is_id_in_queue)

    def test_reservations_should_have_different_ids(self):
        reservation1 = self.usecase.execute(self.store1_id, self.user1_id)
        reservation2 = self.usecase.execute(self.store1_id, self.user1_id)
        r1_id, _, _ = reservation1
        r2_id, _, _ = reservation2

        self.assertNotEqual(r1_id, r2_id)

    def test_reservations_in_different_stores_should_be_in_their_queue(self):
        reservation1 = self.usecase.execute(self.store1_id, self.user1_id)
        reservation2 = self.usecase.execute(self.store2_id, self.user1_id)
        r1_id, _, _ = reservation1
        r2_id, _, _ = reservation2
        is_id1_in_queue1 = r1_id in self.store_provider.get_queue(self.store1_id)
        is_id2_in_queue2 = r2_id in self.store_provider.get_queue(self.store2_id)

        self.assertTrue(is_id1_in_queue1)
        self.assertTrue(is_id2_in_queue2)

    def test_reservations_from_different_users_should_be_in_same_queue(self):
        reservation1 = self.usecase.execute(self.store1_id, self.user1_id)
        reservation2 = self.usecase.execute(self.store1_id, self.user2_id)
        r1_id, _, _ = reservation1
        r2_id, _, _ = reservation2
        is_id1_in_queue = r1_id in self.store_provider.get_queue(self.store1_id)
        is_id2_in_queue = r2_id in self.store_provider.get_queue(self.store1_id)

        self.assertTrue(is_id1_in_queue)
        self.assertTrue(is_id2_in_queue)
        

    def test_should_throw_if_get_queue_throws(self):
        store_provider = MockStoreProvider(throws_on_get=True)
        u = BookUseCase(store_provider, self.reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)

    def test_should_throw_if_set_queue_throws(self):
        store_provider = MockStoreProvider(throws_on_set=True)
        u = BookUseCase(store_provider, self.reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)

    def test_should_throw_if_add_reservation_throws(self):
        reservation_provider = MockReservationProvider(throws_on_add=True)
        u = BookUseCase(self.store_provider, reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None)


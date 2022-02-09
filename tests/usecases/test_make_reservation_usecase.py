import unittest

from tests.usecases.mock_queue_provider import MockQueueProvider

from src.clup.entities.reservation import Reservation
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase


class MockReservationProvider:
    def __init__(self, throws_on_add=False):
        self.reservations = []
        self.throws_on_add = throws_on_add

    def get_reservations(self):
        return self.reservations

    def add_reservation(self, reservation):
        if self.throws_on_add:
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

    def test_reservations_are_stored_in_reservation_provider(self):
        r1_aisle_id = 10
        r2_aisle_id = 20
        r1_id = self.u.execute(self.user1_id, self.store1_id, [r1_aisle_id])
        r2_id = self.u.execute(self.user2_id, self.store2_id, [r2_aisle_id])
        reservations = self.reservation_provider.get_reservations()
        r_ids = [r.id for r in reservations]

        self.assertTrue(r1_id in r_ids)
        self.assertTrue(r2_id in r_ids)

    def test_reservations_should_have_different_ids(self):
        r1_aisle_id = 10
        r2_aisle_id = 20
        r1_id = self.u.execute(self.user1_id, self.store1_id, [r1_aisle_id])
        r2_id = self.u.execute(self.user2_id, self.store2_id, [r2_aisle_id])

        self.assertNotEqual(r1_id, r2_id)

    def test_reservation_for_different_aisles_same_store_has_same_id(self):
        r_aisle1_id = 10
        r_aisle2_id = 20
        aisles = [r_aisle1_id, r_aisle2_id]
        r_id = self.u.execute(self.user1_id, self.store1_id, aisles)
        reservations = self.reservation_provider.get_reservations()
        r1 = Reservation(r_id, r_aisle1_id, self.user1_id)
        r2 = Reservation(r_id, r_aisle2_id, self.user1_id)

        self.assertTrue(r1 in reservations)
        self.assertTrue(r2 in reservations)

    @unittest.skip('to fix')
    def test_inconsistent_aisle_ids_and_store_id_throws(self):
        pass

    def test_reservation_id_should_be_in_pools_if_aisle_pool_is_not_full(self):
        aisle_id = 10
        self.queue_provider.get_aisle_pool(aisle_id).capacity = 5

        r_id = self.u.execute(self.user1_id, self.store1_id, [aisle_id])
        aisle_pool = self.queue_provider.get_aisle_pool(aisle_id)
        store_pool = self.queue_provider.get_store_pool(self.store1_id)
        queue = self.queue_provider.get_waiting_queue(aisle_id)

        self.assertTrue(r_id in aisle_pool)
        self.assertTrue(r_id in store_pool.pool)
        self.assertTrue(r_id not in queue)

    def test_reservation_id_should_be_in_queue_if_pool_is_full(self):
        aisle_id = 10
        self.queue_provider.get_aisle_pool(aisle_id).capacity = 0

        r_id = self.u.execute(self.user1_id, self.store1_id, [aisle_id])
        aisle_pool = self.queue_provider.get_aisle_pool(aisle_id)
        store_pool = self.queue_provider.get_store_pool(self.store1_id)
        queue = self.queue_provider.get_waiting_queue(aisle_id)

        self.assertTrue(r_id not in aisle_pool)
        self.assertTrue(r_id not in store_pool.pool)
        self.assertTrue(r_id in queue)

    def test_reservation_id_should_be_in_queue_after_pool_is_filled(self):
        aisle_id = 10
        self.queue_provider.get_aisle_pool(aisle_id).capacity = 1

        r1_id = self.u.execute(self.user1_id, self.store1_id, [aisle_id])
        r2_id = self.u.execute(self.user2_id, self.store1_id, [aisle_id])
        aisle_pool = self.queue_provider.get_aisle_pool(aisle_id)
        store_pool = self.queue_provider.get_store_pool(self.store1_id)
        queue = self.queue_provider.get_waiting_queue(aisle_id)

        self.assertTrue(r1_id in aisle_pool)
        self.assertTrue(r1_id in store_pool.pool)
        self.assertTrue(r2_id in queue)

    def test_different_users_reservations_should_be_in_same_queue(self):
        aisle_id = 10
        self.queue_provider.get_aisle_pool(aisle_id).capacity = 0

        r1_id = self.u.execute(self.user1_id, self.store1_id, [aisle_id])
        r2_id = self.u.execute(self.user2_id, self.store1_id, [aisle_id])
        queue = self.queue_provider.get_waiting_queue(aisle_id)

        self.assertTrue(r1_id in queue)
        self.assertTrue(r2_id in queue)

    def test_should_throw_if_add_reservation_throws(self):
        reservation_provider = MockReservationProvider(throws_on_add=True)
        u = MakeReservationUseCase(self.queue_provider, reservation_provider)

        with self.assertRaises(ValueError):
            u.execute(None, None, ['a'])


class TestMakeReservationUseCaseMultipleAisles(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockQueueProvider()
        self.reservation_provider = MockReservationProvider()
        self.u = MakeReservationUseCase(
            self.queue_provider, self.reservation_provider)

    def test_reservation_id_should_be_in_pools_if_aisle_pools_are_not_full(self):
        user_id = 1
        store_id = 100
        aisle1_id = 10
        self.queue_provider.get_aisle_pool(aisle1_id).capacity = 5
        aisle2_id = 20
        self.queue_provider.get_aisle_pool(aisle2_id).capacity = 5
        aisles = [aisle1_id, aisle2_id]

        r_id = self.u.execute(user_id, store_id, aisles)
        aisle1_pool = self.queue_provider.get_aisle_pool(aisle1_id)
        aisle2_pool = self.queue_provider.get_aisle_pool(aisle2_id)
        store_pool = self.queue_provider.get_store_pool(store_id)
        queue1 = self.queue_provider.get_waiting_queue(aisle1_id)
        queue2 = self.queue_provider.get_waiting_queue(aisle2_id)

        self.assertTrue(r_id in aisle1_pool)
        self.assertTrue(r_id in aisle2_pool)
        self.assertEqual(len(store_pool.pool), 1)
        self.assertTrue(r_id in store_pool.pool)
        self.assertTrue(r_id not in queue1)
        self.assertTrue(r_id not in queue2)
        
    def test_reservation_id_should_be_in_queues_if_aisle_pools_are_full(self):
        user_id = 1
        store_id = 100
        aisle1_id = 10
        self.queue_provider.get_aisle_pool(aisle1_id).capacity = 0
        aisle2_id = 20
        self.queue_provider.get_aisle_pool(aisle2_id).capacity = 0
        aisles = [aisle1_id, aisle2_id]

        r_id = self.u.execute(user_id, store_id, aisles)
        aisle1_pool = self.queue_provider.get_aisle_pool(aisle1_id)
        aisle2_pool = self.queue_provider.get_aisle_pool(aisle2_id)
        store_pool = self.queue_provider.get_store_pool(store_id)
        queue1 = self.queue_provider.get_waiting_queue(aisle1_id)
        queue2 = self.queue_provider.get_waiting_queue(aisle2_id)

        self.assertTrue(r_id not in aisle1_pool)
        self.assertTrue(r_id not in aisle2_pool)
        self.assertTrue(r_id not in store_pool.pool)
        self.assertTrue(r_id in queue1)
        self.assertTrue(r_id in queue2)
    
    def test_reservation_id_in_store_pool_only_if_also_in_interested_aisle_pools(self):
        user_id = 1
        store_id = 100
        aisle1_id = 10
        self.queue_provider.get_aisle_pool(aisle1_id).capacity = 5
        aisle2_id = 20
        self.queue_provider.get_aisle_pool(aisle2_id).capacity = 0
        aisles = [aisle1_id, aisle2_id]

        r_id = self.u.execute(user_id, store_id, aisles)
        aisle1_pool = self.queue_provider.get_aisle_pool(aisle1_id)
        aisle2_pool = self.queue_provider.get_aisle_pool(aisle2_id)
        store_pool = self.queue_provider.get_store_pool(store_id)
        queue1 = self.queue_provider.get_waiting_queue(aisle1_id)
        queue2 = self.queue_provider.get_waiting_queue(aisle2_id)

        self.assertTrue(r_id in aisle1_pool)
        self.assertTrue(r_id not in aisle2_pool)
        self.assertTrue(r_id not in store_pool.pool)
        self.assertTrue(r_id not in queue1)
        self.assertTrue(r_id in queue2)

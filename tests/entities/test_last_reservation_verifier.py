import unittest

from tests.usecases.mock_queue_provider import MockQueueProvider
from tests.usecases.mock_reservation_provider import MockReservationProvider

from src.clup.entities.reservation import Reservation
from src.clup.entities.last_reservation_verifier import LastReservationVerifier


class TestLastReservationVerifier(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockQueueProvider()
        self.reservation_provider = MockReservationProvider()
        self.verifier = LastReservationVerifier(self.queue_provider, self.reservation_provider)
        
    def test_unexistent_reservation_throws(self):
        invalid_reservation_id = -1

        with self.assertRaises(ValueError):
            self.verifier.is_last(invalid_reservation_id)

    def test_existent_reservation_not_in_active_pool_gives_false(self):
        aisle_id = 2
        reservation_id = 1
        reservation = Reservation(reservation_id, aisle_id, 3)
        self.reservation_provider.add_reservation(reservation)

        is_last = self.verifier.is_last(reservation_id)

        self.assertFalse(is_last)
        
    def test_existent_reservation_in_active_pool_gives_true(self):
        aisle_id = 2
        reservation_id = 1
        reservation = Reservation(reservation_id, aisle_id, 3)
        self.reservation_provider.add_reservation(reservation)
        pool = self.queue_provider.get_active_pool(aisle_id)
        pool.capacity = 5
        pool.add(reservation_id)

        is_last = self.verifier.is_last(reservation_id)

        self.assertTrue(is_last)

    def test_existent_reservation_not_in_all_selected_active_pools_gives_false(self):
        aisle1_id = 20
        aisle2_id = 30
        reservation_id = 1
        reservation1 = Reservation(reservation_id, aisle1_id, 3)
        reservation2 = Reservation(reservation_id, aisle2_id, 3)
        self.reservation_provider.add_reservation(reservation2)
        self.reservation_provider.add_reservation(reservation1)
        aisle1_pool = self.queue_provider.get_active_pool(aisle1_id)
        aisle1_pool.capacity = 5
        aisle1_pool.add(reservation_id)

        is_last = self.verifier.is_last(reservation_id)

        self.assertFalse(is_last)

    def test_existent_reservation_not_in_all_selected_active_pools_gives_true(self):
        aisle1_id = 20
        aisle2_id = 30
        reservation_id = 1
        reservation1 = Reservation(reservation_id, aisle1_id, 3)
        reservation2 = Reservation(reservation_id, aisle2_id, 3)
        self.reservation_provider.add_reservation(reservation2)
        self.reservation_provider.add_reservation(reservation1)
        aisle1_pool = self.queue_provider.get_active_pool(aisle1_id)
        aisle1_pool.capacity = 5
        aisle1_pool.add(reservation_id)
        aisle2_pool = self.queue_provider.get_active_pool(aisle2_id)
        aisle2_pool.capacity = 5
        aisle2_pool.add(reservation_id)

        is_last = self.verifier.is_last(reservation_id)

        self.assertTrue(is_last)

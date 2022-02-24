import unittest

from src.clup.entities.reservation import Reservation
from src.clup.usecases.admin.consume_reservation_usecase \
    import ConsumeReservationUseCase
from tests.usecases.mock_lane_provider import MockLaneProvider
from tests.usecases.mock_reservation_provider import MockReservationProvider


class TestConsumeReservationUseCase(unittest.TestCase):
    def setUp(self):
        self.lane_provider = MockLaneProvider()
        self.reservation_provider = MockReservationProvider()
        self.u = ConsumeReservationUseCase(
            self.lane_provider, self.reservation_provider)

    def test_reservation_removed_from_aisle_pool_and_moved_to_to_free(self):
        store_id = 1
        aisle_id = 10
        reservation_id = 2
        reservation = Reservation(reservation_id, aisle_id, 100)
        aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
        aisle_pool.capacity = 5
        aisle_pool.add(reservation_id)
        qt = aisle_pool.current_quantity
        store_pool = self.lane_provider.get_store_pool(store_id)
        store_pool.add(reservation_id)
        self.reservation_provider.add_reservation(reservation)

        self.u.execute(store_id, reservation_id)

        self.assertTrue(reservation_id not in aisle_pool)
        self.assertEqual(aisle_pool.current_quantity, qt + 1)
        self.assertTrue(reservation_id not in store_pool.enabled)
        self.assertTrue(reservation_id in store_pool.to_free)

    def test_throws_if_reservation_is_not_present(self):
        store_id = 1
        reservation_id = 2
        pool = self.lane_provider.get_aisle_pool(store_id)
        pool.capacity = 5
        pool.add(reservation_id)

        with self.assertRaises(ValueError):
            self.u.execute(store_id, -1)

    def test_reservation_moved_from_multiple_aisle_pools_to_to_free(self):
        store_id = 1
        aisle1_id = 10
        aisle1_id = 10
        aisle2_id = 20
        reservation_id = 2
        reservation1 = Reservation(reservation_id, aisle1_id, 100)
        reservation2 = Reservation(reservation_id, aisle2_id, 100)
        aisle1_pool = self.lane_provider.get_aisle_pool(aisle1_id)
        aisle2_pool = self.lane_provider.get_aisle_pool(aisle2_id)
        aisle1_pool.capacity = 5
        aisle1_pool.add(reservation_id)
        aisle2_pool.capacity = 5
        aisle2_pool.add(reservation_id)
        qt1 = aisle1_pool.current_quantity
        qt2 = aisle2_pool.current_quantity
        store_pool = self.lane_provider.get_store_pool(store_id)
        store_pool.add(reservation_id)
        self.reservation_provider.add_reservation(reservation1)
        self.reservation_provider.add_reservation(reservation2)

        self.u.execute(store_id, reservation_id)

        self.assertTrue(reservation_id not in store_pool.enabled)
        self.assertTrue(reservation_id in store_pool.to_free)
        self.assertTrue(reservation_id not in aisle1_pool)
        self.assertTrue(reservation_id not in aisle2_pool)
        self.assertEqual(aisle1_pool.current_quantity, qt1 + 1)
        self.assertEqual(aisle2_pool.current_quantity, qt2 + 1)

import unittest

from src.clup.usecases.consume_reservation_usecase \
    import ConsumeReservationUseCase
from tests.usecases.mock_queue_provider import MockQueueProvider


class TestConsumeReservationUseCase(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockQueueProvider()
        self.u = ConsumeReservationUseCase(self.queue_provider)

    def test_reservation_removed_from_active_pool(self):
        store_id = 1
        reservation_id = 2
        pool = self.queue_provider.get_aisle_pool(store_id)
        pool.capacity = 5
        pool.add(reservation_id)
        qt = pool.current_quantity

        self.u.execute(store_id, reservation_id)

        self.assertTrue(reservation_id not in pool)
        self.assertEqual(pool.current_quantity, qt + 1)

    def test_throws_if_reservation_is_not_present(self):
        store_id = 1
        reservation_id = 2
        pool = self.queue_provider.get_aisle_pool(store_id)
        pool.capacity = 5
        pool.add(reservation_id)

        with self.assertRaises(ValueError):
            self.u.execute(store_id, -1)

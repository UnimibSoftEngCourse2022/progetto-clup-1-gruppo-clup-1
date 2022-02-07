from collections import defaultdict
import unittest

from tests.usecases.mock_reservation_provider import MockReservationProvider
from tests.usecases.mock_queue_provider import MockQueueProvider

from src.clup.providers.aisle_provider_abc import AisleProvider
from src.clup.entities.store_active_pool import StoreActivePool
from src.clup.entities.reservation import Reservation


class MockAislesProvider(AisleProvider):
    def __init__(self):
        self.aisles = defaultdict(list())

    def get_store_aisles(self, store_id):
        return self.aisles[store_id]

class TestStoreActivePool(unittest.TestCase):
    def setUp(self):
        self.sap = StoreActivePool()
        self.queue_provider = MockQueueProvider()
        self.reservation_provider = MockReservationProvider()

    def test_is_empty_after_init(self):
        self.assertEqual(len(self.sap.pool), 0)
        self.assertEqual(len(self.sap.to_free), 0)

    def test_add_increments_length(self):
        self.sap.add('a')

        self.assertTrue(len(self.sap.pool) == 1)

    def test_added_elements_are_in_pool(self):
        self.sap.add('a')
        self.sap.add('b')

        self.assertTrue('a' in self.sap.pool)
        self.assertTrue('b' in self.sap.pool)
        self.assertFalse('c' in self.sap.pool)

    def test_consume_moves_element_from_pool_to_to_free(self):
        reservation_id = 1
        self.sap.add(reservation_id)

        self.sap.consume(reservation_id)

        self.assertTrue(reservation_id not in self.sap.pool)
        self.assertTrue(reservation_id in self.sap.to_free)


    def test_consume_calls_consume_on_reservation_aisles(self):
        reservation_id = 1
        aisle1_id = 10
        aisle2_id = 20
        r1 = Reservation(reservation_id, aisle1_id, 3)
        r2 = Reservation(reservation_id, aisle2_id, 3)
        self.reservation_provider.add_reservation(r1)
        self.reservation_provider.add_reservation(r2)
        pool1 = self.queue_provider.get_active_pool(aisle1_id)
        pool1.capacity = 5
        pool1.add(reservation_id1)
        qt1 = pool1.current_quantity
        pool2 = self.queue_provider.get_active_pool(aisle2_id)
        pool2.capacity = 5
        pool2.add(reservation_id1)
        qt2 = pool1.current_quantity

        self.sap.consume(reservation_id)

        self.assertEqual(pool1.current_quantity, qt1 + 1)
        self.assertEqual(pool2.current_quantity, qt2 + 1)

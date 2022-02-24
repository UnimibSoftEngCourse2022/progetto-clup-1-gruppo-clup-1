import unittest

from src.clup.entities.exceptions import EmptyPoolError
from src.clup.entities.reservation import Reservation
from src.clup.usecases.admin.free_reservation_usecase import FreeReservationUseCase
from tests.usecases.mock_lane_provider import MockLaneProvider
from tests.usecases.mock_reservation_provider import MockReservationProvider


class TestFreeReservationUseCase(unittest.TestCase):
    def consume_in_aisle(self, aisle_id, reservation_id):
        aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
        aisle_pool.capacity = 1
        aisle_pool.add(reservation_id)
        aisle_pool.consume(reservation_id)
        return aisle_pool

    def consume_in_store(self, store_id, reservation_id):
        store_pool = self.lane_provider.get_store_pool(store_id)
        store_pool.add(reservation_id)
        store_pool.consume(reservation_id)
        return store_pool

    def setUp(self):
        self.lane_provider = MockLaneProvider()
        self.reservation_provider = MockReservationProvider()
        self.u = FreeReservationUseCase(
            self.lane_provider, self.reservation_provider)

    def test_aisle_pool_current_quantity_is_decremented(self):
        aisle_id = 1
        store_id = 10
        reservation_id = 100
        r = Reservation(reservation_id, aisle_id, 200)
        self.reservation_provider.add_reservation(r)
        aisle_pool = self.consume_in_aisle(aisle_id, reservation_id)
        quantity = aisle_pool.current_quantity
        store_pool = self.consume_in_store(store_id, reservation_id)

        self.u.execute(store_id, reservation_id)

        self.assertEqual(aisle_pool.current_quantity, quantity - 1)
        self.assertTrue(reservation_id not in store_pool.to_free)

    def test_emptypoolerror_is_forwarded(self):
        aisle_id = 1
        store_id = 10
        reservation_id = 100
        r = Reservation(reservation_id, aisle_id, 200)
        self.reservation_provider.add_reservation(r)

        with self.assertRaises(EmptyPoolError):
            self.u.execute(store_id, reservation_id)

    def test_first_element_in_queue_is_popped_into_pool(self):
        aisle_id = 1
        store_id = 10
        reservation_id = 100
        r = Reservation(reservation_id, aisle_id, 200)
        self.reservation_provider.add_reservation(r)
        aisle_pool = self.consume_in_aisle(aisle_id, reservation_id)
        store_pool = self.consume_in_store(store_id, reservation_id)
        queue = self.lane_provider.get_waiting_queue(aisle_id)
        queue.push(200)
        queue.push(300)

        self.u.execute(store_id, reservation_id)

        self.assertTrue(200 in aisle_pool)
        self.assertTrue(200 in store_pool.enabled)
        self.assertTrue(300 in queue)

    def test_pool_is_unchanged_if_queue_is_empty(self):
        aisle_id = 1
        store_id = 10
        reservation_id = 100
        r = Reservation(reservation_id, aisle_id, 200)
        self.reservation_provider.add_reservation(r)
        aisle_pool = self.consume_in_aisle(aisle_id, reservation_id)
        store_pool = self.consume_in_store(store_id, reservation_id)

        self.u.execute(store_id, reservation_id)

        self.assertEqual(len(aisle_pool), 0)
        self.assertEqual(len(store_pool.enabled), 0)

    def test_multiple_aisle_pools_quantity_is_decremented(self):
        aisle1_id = 1
        aisle2_id = 2
        store_id = 10
        reservation_id = 100
        r1 = Reservation(reservation_id, aisle1_id, 200)
        r2 = Reservation(reservation_id, aisle2_id, 200)
        self.reservation_provider.add_reservation(r1)
        self.reservation_provider.add_reservation(r2)
        aisle1_pool = self.consume_in_aisle(aisle1_id, reservation_id)
        aisle2_pool = self.consume_in_aisle(aisle2_id, reservation_id)
        quantity1 = aisle1_pool.current_quantity
        quantity2 = aisle2_pool.current_quantity
        store_pool = self.consume_in_store(store_id, reservation_id)

        self.u.execute(store_id, reservation_id)

        self.assertEqual(aisle1_pool.current_quantity, quantity1 - 1)
        self.assertEqual(aisle2_pool.current_quantity, quantity2 - 1)
        self.assertTrue(reservation_id not in store_pool.to_free)

    def test_first_element_in_queues_popped_to_pools(self):
        aisle1_id = 1
        aisle2_id = 2
        store_id = 10
        reservation_id = 100
        r1 = Reservation(reservation_id, aisle1_id, 200)
        r2 = Reservation(reservation_id, aisle2_id, 200)
        self.reservation_provider.add_reservation(r1)
        self.reservation_provider.add_reservation(r2)
        aisle1_pool = self.consume_in_aisle(aisle1_id, reservation_id)
        aisle2_pool = self.consume_in_aisle(aisle2_id, reservation_id)
        store_pool = self.consume_in_store(store_id, reservation_id)
        queue1 = self.lane_provider.get_waiting_queue(aisle1_id)
        queue1.push(200)
        queue1.push(300)
        queue2 = self.lane_provider.get_waiting_queue(aisle2_id)
        queue2.push(200)
        queue2.push(300)

        self.u.execute(store_id, reservation_id)

        self.assertTrue(200 in aisle1_pool)
        self.assertTrue(200 in aisle2_pool)
        self.assertTrue(200 in store_pool.enabled)
        self.assertEqual(len(store_pool.enabled), 1)
        self.assertTrue(300 not in aisle1_pool)
        self.assertTrue(300 not in aisle2_pool)

    def test_no_elements_are_popped_if_queues_are_empty(self):
        aisle1_id = 1
        aisle2_id = 2
        store_id = 10
        reservation_id = 100
        r1 = Reservation(reservation_id, aisle1_id, 200)
        r2 = Reservation(reservation_id, aisle2_id, 200)
        self.reservation_provider.add_reservation(r1)
        self.reservation_provider.add_reservation(r2)
        aisle1_pool = self.consume_in_aisle(aisle1_id, reservation_id)
        aisle2_pool = self.consume_in_aisle(aisle2_id, reservation_id)
        store_pool = self.consume_in_store(store_id, reservation_id)

        self.u.execute(store_id, reservation_id)

        self.assertEqual(len(aisle1_pool), 0)
        self.assertEqual(len(aisle2_pool), 0)
        self.assertEqual(len(store_pool.enabled), 0)

    def test_element_in_one_queue_only_popped_to_pools(self):
        aisle1_id = 1
        aisle2_id = 2
        store_id = 10
        reservation1_id = 100
        reservation2_id = 200
        reservation3_id = 300
        reservation4_id = 400
        r1_1 = Reservation(reservation1_id, aisle1_id, 1000)
        r1_2 = Reservation(reservation1_id, aisle2_id, 1000)
        r2_1 = Reservation(reservation2_id, aisle1_id, 2000)
        r2_2 = Reservation(reservation2_id, aisle2_id, 2000)
        r3_1 = Reservation(reservation3_id, aisle1_id, 3000)
        r4_2 = Reservation(reservation4_id, aisle2_id, 4000)
        self.reservation_provider.add_reservation(r1_1)
        self.reservation_provider.add_reservation(r1_2)
        self.reservation_provider.add_reservation(r2_1)
        self.reservation_provider.add_reservation(r2_2)
        self.reservation_provider.add_reservation(r3_1)
        self.reservation_provider.add_reservation(r4_2)
        aisle1_pool = self.consume_in_aisle(aisle1_id, reservation1_id)
        aisle2_pool = self.consume_in_aisle(aisle2_id, reservation1_id)
        store_pool = self.consume_in_store(store_id, reservation1_id)
        queue1 = self.lane_provider.get_waiting_queue(aisle1_id)
        queue1.push(reservation2_id)
        queue1.push(reservation3_id)
        queue2 = self.lane_provider.get_waiting_queue(aisle2_id)
        queue2.push(reservation4_id)
        queue2.push(reservation2_id)

        self.u.execute(store_id, reservation1_id)

        self.assertTrue(reservation2_id in aisle1_pool)
        self.assertTrue(reservation4_id in aisle2_pool)
        self.assertTrue(reservation4_id in store_pool.enabled)
        self.assertEqual(len(store_pool.enabled), 1)

    def test_element_in_popped_to_pools_only_after_in_all_its_pools(self):
        aisle1_id = 1
        aisle2_id = 2
        store_id = 10
        reservation1_id = 100
        reservation2_id = 200
        reservation3_id = 300
        reservation4_id = 400
        r1_1 = Reservation(reservation1_id, aisle1_id, 1000)
        r1_2 = Reservation(reservation1_id, aisle2_id, 1000)
        r2_1 = Reservation(reservation2_id, aisle1_id, 2000)
        r2_2 = Reservation(reservation2_id, aisle2_id, 2000)
        r3_1 = Reservation(reservation3_id, aisle1_id, 3000)
        r4_2 = Reservation(reservation4_id, aisle2_id, 4000)
        self.reservation_provider.add_reservation(r1_1)
        self.reservation_provider.add_reservation(r1_2)
        self.reservation_provider.add_reservation(r2_1)
        self.reservation_provider.add_reservation(r2_2)
        self.reservation_provider.add_reservation(r3_1)
        self.reservation_provider.add_reservation(r4_2)
        aisle1_pool = self.consume_in_aisle(aisle1_id, reservation1_id)
        aisle2_pool = self.consume_in_aisle(aisle2_id, reservation1_id)
        store_pool = self.consume_in_store(store_id, reservation1_id)
        queue1 = self.lane_provider.get_waiting_queue(aisle1_id)
        queue1.push(reservation2_id)
        queue1.push(reservation3_id)
        aisle2_pool.capacity = 2
        aisle2_pool.add(reservation2_id)
        queue2 = self.lane_provider.get_waiting_queue(aisle2_id)
        queue2.push(reservation4_id)

        self.u.execute(store_id, reservation1_id)

        self.assertTrue(reservation2_id in aisle1_pool)
        self.assertTrue(reservation2_id in aisle2_pool)
        self.assertTrue(reservation2_id in store_pool.enabled)
        self.assertTrue(reservation4_id in store_pool.enabled)
        self.assertEqual(len(store_pool.enabled), 2)

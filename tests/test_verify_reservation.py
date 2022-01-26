import unittest
from src.clup.verify_reservation_usecase import verify_reservation
from src.clup.book_usecase import book


class TestBookUsecase(unittest.TestCase):
    def test_reservation_valid(self):
        market_id = 1
        queue = ()
        reservation, queue = book(market_id, queue)
        reservation_id, _ = reservation
        is_reservation_valid = verify_reservation(reservation_id, queue)
        self.assertTrue(is_reservation_valid)

    def test_reservation_not_valid_for_different_queue(self):
        market_id = 1
        queue1 = ()
        queue2 = ()
        reservation, queue1 = book(market_id, queue1)
        reservation1_id, _ = reservation
        is_reservation_valid_for_different_queue = verify_reservation(reservation1_id, queue2)
        self.assertFalse(is_reservation_valid_for_different_queue)

    def test_reservation_with_multiple_queue(self):
        market1_id = 1
        market2_id = 2
        queue1 = ()
        queue2 = ()
        reservation1, queue1 = book(market1_id, queue1)
        reservation2, queue2 = book(market2_id, queue2)
        reservation1_id, _ = reservation1
        reservation2_id, _ = reservation2
        is_reservation1_valid_for_queue1 = verify_reservation(reservation1_id, queue1)
        is_reservation2_valid_for_queue2 = verify_reservation(reservation2_id, queue2)
        is_reservation1_valid_for_queue2 = verify_reservation(reservation1_id, queue2)
        is_reservation2_valid_for_queue1 = verify_reservation(reservation2_id, queue1)
        self.assertTrue(is_reservation1_valid_for_queue1)
        self.assertTrue(is_reservation2_valid_for_queue2)
        self.assertFalse(is_reservation1_valid_for_queue2)
        self.assertFalse(is_reservation2_valid_for_queue1)
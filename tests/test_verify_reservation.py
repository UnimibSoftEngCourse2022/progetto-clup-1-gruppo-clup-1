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


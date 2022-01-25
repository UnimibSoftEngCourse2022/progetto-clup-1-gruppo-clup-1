import unittest

from src.clup.book_usecase import book

class TestBookUsecase(unittest.TestCase):
    def test_book_in_that_market(self):
        market_id = 1
        
        reservation, _ = book(market_id, ())
        _, reservation_market_id = reservation
        
        self.assertEqual(reservation_market_id, market_id)

    def test_book_in_two_market_should_have_different_ids(self):
        market1_id = 1
        market2_id = 2
        
        reservation1, _ = book(market1_id, ())
        _, reservation_market1_id = reservation1
        
        reservation2, _ = book(market2_id, ())
        _, reservation_market2_id = reservation2

        self.assertEqual(reservation_market1_id, market1_id)
        self.assertEqual(reservation_market2_id, market2_id)

    def test_book_id_is_the_updated_queue(self):
        queue = ()
        
        reservation, updated_queue = book(None, queue)
        reservation_id, _ = reservation
        is_id_in_queue = reservation_id in updated_queue
        
        self.assertTrue(is_id_in_queue)

    def test_different_book_should_have_different_ids_and_be_in_the_queue(self):
        queue = ()
        
        reservation1, queue = book(None, queue)
        reservation2, queue = book(None, queue)
        reservation1_id, _ = reservation1
        reservation2_id, _ = reservation2
        is_id1_in_queue = reservation1_id in queue
        is_id2_in_queue = reservation2_id in queue

        self.assertTrue(is_id1_in_queue)
        self.assertTrue(is_id2_in_queue)
        self.assertNotEqual(reservation1_id, reservation2_id)
        
    def test_book_should_not_alter_original_queue(self):
        queue = ()
        
        _, updated_queue = book(None, queue)

        self.assertNotEqual(updated_queue, queue)

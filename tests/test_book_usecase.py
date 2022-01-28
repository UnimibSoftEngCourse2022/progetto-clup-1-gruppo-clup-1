import unittest

from src.clup.book_usecase import BookUseCase


class MockStoreProvider:
    def __init__(self):
        self.queue = ()

    def set_queue(self, store_id, queue):
        self.queue = queue

    def get_queue(self, store_id):
        return self.queue


class TestBookUsecase(unittest.TestCase):
    def setUp(self):
        self.store1_id = 1
        self.store2_id = 2

    def test_reservation_contains_store_id(self):
        mock_store_provider = MockStoreProvider()
        b = BookUseCase(mock_store_provider)

        reservation = b.execute(self.store1_id)
        _, reservation_store_id = reservation

        self.assertEqual(reservation_store_id, self.store1_id)

    def test_reservation_in_two_market_should_have_different_store_ids(self):
        mock_store_provider = MockStoreProvider()
        b = BookUseCase(mock_store_provider)

        reservation1 = b.execute(self.store1_id)
        _, reservation_store1_id = reservation1
        reservation2 = b.execute(self.store2_id)
        _, reservation_store2_id = reservation2

        self.assertEqual(reservation_store1_id , self.store1_id)
        self.assertEqual(reservation_store2_id , self.store2_id)

    def test_reservation_should_be_in_the_queue_of_the_store(self):
        store_provider = MockStoreProvider()
        b = BookUseCase(store_provider)

        r_id, r_store_id = b.execute(self.store1_id)
        is_id_in_queue = r_id in store_provider.get_queue(r_store_id)

        self.assertTrue(is_id_in_queue)

    def test_reservations_should_have_different_ids_and_be_in_their_queue(self):
        store_provider = MockStoreProvider()
        b = BookUseCase(store_provider)

        reservation1 = b.execute(self.store1_id)
        reservation2 = b.execute(self.store1_id)
        r1_id, _ = reservation1
        r2_id, _ = reservation2
        is_id1_in_queue = r1_id in store_provider.get_queue(self.store1_id)
        is_id2_in_queue = r2_id in store_provider.get_queue(self.store1_id)

        self.assertTrue(is_id1_in_queue)
        self.assertTrue(is_id2_in_queue)
        self.assertNotEqual(r1_id, r2_id)




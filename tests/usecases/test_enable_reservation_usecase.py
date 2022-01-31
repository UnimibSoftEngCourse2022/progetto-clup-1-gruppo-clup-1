import unittest

from src.clup.usecases.enable_reservation_usecase \
    import EnableReservationUseCase


class MockStoreProvider:
    def __init__(self):
        self.queue = ()

    def set_queue(self, store_id, queue):
        self.queue = queue

    def get_queue(self, store_id):
        return self.queue


class TestConsumeReservation(unittest.TestCase):
    def test_use_valid_reservation(self):
        store_id = 1
        store_provider = MockStoreProvider()
        reservation_id = 12
        queue = (reservation_id,)
        store_provider.set_queue(store_id, queue)
        c = EnableReservationUseCase(store_provider)
        reservation = (reservation_id, store_id)
        success = c.execute(reservation)
        is_id_in_queue = reservation_id in store_provider.get_queue(store_id)

        self.assertFalse(is_id_in_queue)
        self.assertTrue(success)

    def test_use_invalid_reservation(self):
        store_id = 1
        store_provider = MockStoreProvider()
        valid_id = 12
        invalid_id = 13

        queue = (valid_id,)
        store_provider.set_queue(store_id, queue)
        c = EnableReservationUseCase(store_provider)
        invalid_reservation = (invalid_id, store_id)

        success = c.execute(invalid_reservation)
        is_id_in_queue = valid_id in store_provider.get_queue(store_id)

        self.assertTrue(is_id_in_queue)
        self.assertFalse(success)

import unittest

from src.clup.entities.reservation import Reservation
from src.clup.providers.basic_reservation_provider \
    import BasicReservationProvider


class TestBasicReservationProvider(unittest.TestCase):
    def setUp(self):
        self.brp = BasicReservationProvider()

    def test_is_empty_after_initialization(self):
        reservations = self.brp.get_reservations()

        self.assertTrue(len(reservations) == 0)

    def test_reservation_is_added(self):
        r = Reservation(1, 2, 3)

        self.brp.add_reservation(r)

        self.assertTrue(r in self.brp.get_reservations())

    def test_add_of_multiple_reservations(self):
        r1 = Reservation(1, 2, 3)
        r2 = Reservation(4, 5, 6)

        self.brp.add_reservation(r1)
        self.brp.add_reservation(r2)

        self.assertTrue(r1 in self.brp.get_reservations())
        self.assertTrue(r2 in self.brp.get_reservations())

    def test_add_reservations_with_same_id_throws(self):
        r1 = Reservation(1, 2, 3)
        r2 = Reservation(1, 4, 5)

        self.brp.add_reservation(r1)

        with self.assertRaises(ValueError):
            self.brp.add_reservation(r2)

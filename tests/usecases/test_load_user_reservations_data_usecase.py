import unittest

from tests.usecases.mock_aisle_provider import MockAisleProvider
from tests.usecases.mock_reservation_provider import MockReservationProvider
from tests.usecases.mock_store_provider import MockStoreProvider

from src.clup.entities.aisle import Aisle
from src.clup.entities.reservation import Reservation
from src.clup.entities.store import Store
from src.clup.usecases.load_user_reservations_data_usecase \
    import LoadUserReservationsDataUseCase


class TestLoadUserReservationsDataUseCase(unittest.TestCase):
    def setUp(self):
        self.reservation_provider = MockReservationProvider()
        self.store_provider = MockStoreProvider()
        self.aisle_provider = MockAisleProvider()
        self.u = LoadUserReservationsDataUseCase(self.reservation_provider,
                                                 self.store_provider,
                                                 self.aisle_provider)

    def test_empty_sequence_returned_on_no_reservations(self):
        reservations_data = self.u.execute('user_id')

        self.assertEqual(len(reservations_data), 0)

    def test_store_with_reserved_aisles_returned(self):
        store = Store('store_id', 'name', 'address')
        aisle1 = Aisle('aisle1_id', 'a1', 'cat1')
        aisle2 = Aisle('aisle2_id', 'a2', 'cat2')
        r1 = Reservation('r1', 'aisle1_id', 'user_id')
        r2 = Reservation('r1', 'aisle2_id', 'user_id')
        self.store_provider.stores.append(store)
        self.aisle_provider.aisles['store_id'] = [aisle1, aisle2]
        self.reservation_provider.reservations.extend([r1, r2])

        reservations_data = self.u.execute('user_id')

        self.assertEqual(len(reservations_data), 1)
        r_id, r_store, r_aisles = reservations_data[0]
        self.assertEqual(r_id, 'r1')
        self.assertEqual(r_store, store)
        self.assertEqual(r_aisles, [aisle1, aisle2])

    def test_stores_with_reserved_aisles_returned(self):
        store1 = Store('store1_id', 'name', 'address')
        aisle1 = Aisle('aisle1_id', 'a1', 'cat1')
        aisle2 = Aisle('aisle2_id', 'a2', 'cat2')
        r1 = Reservation('r1', 'aisle1_id', 'user_id')
        r2 = Reservation('r1', 'aisle2_id', 'user_id')
        self.store_provider.stores.append(store1)
        self.aisle_provider.aisles['store1_id'] = [aisle1, aisle2]
        self.reservation_provider.reservations.extend([r1, r2])
        store2 = Store('store2_id', 'name', 'address')
        aisle3 = Aisle('aisle3_id', 'a4', 'cat4')
        aisle4 = Aisle('aisle4_id', 'a3', 'cat3')
        r3 = Reservation('r2', 'aisle3_id', 'user_id')
        r4 = Reservation('r2', 'aisle4_id', 'user_id')
        self.store_provider.stores.append(store2)
        self.aisle_provider.aisles['store2_id'] = [aisle3, aisle4]
        self.reservation_provider.reservations.extend([r3, r4])

        reservations_data = self.u.execute('user_id')

        self.assertEqual(len(reservations_data), 2)

    def test_multiple_reservations_in_store_counted(self):
        store1 = Store('store1_id', 'name', 'address')
        aisle1 = Aisle('aisle1_id', 'a1', 'cat1')
        aisle2 = Aisle('aisle2_id', 'a2', 'cat2')
        r1 = Reservation('r1', 'aisle1_id', 'user_id')
        r2 = Reservation('r1', 'aisle2_id', 'user_id')
        self.store_provider.stores.append(store1)
        self.aisle_provider.aisles['store1_id'] = [aisle1, aisle2]
        self.reservation_provider.reservations.extend([r1, r2])
        r3 = Reservation('r2', 'aisle1_id', 'user_id')
        r4 = Reservation('r2', 'aisle2_id', 'user_id')
        self.reservation_provider.reservations.extend([r3, r4])

        reservations_data = self.u.execute('user_id')

        self.assertEqual(len(reservations_data), 2)

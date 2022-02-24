import unittest

from src.clup.entities.aisle import Aisle
from src.clup.entities.aisle_pool import AislePool
from src.clup.entities.reservation import Reservation
from src.clup.entities.store import Store
from src.clup.entities.store_pool import StorePool
from src.clup.usecases.system.remove_unused_reservation import RemoveUnusedReservation


class MockStoreProvider:
    def __init__(self):
        self.stores = {}

    def get_stores(self):
        return self.stores.values()


class MockLaneProvider:
    def __init__(self):
        self.store_pools = {}
        self.aisle_pools = {}

    def get_aisle_pool(self, aisle_id):
        return self.aisle_pools[aisle_id]

    def get_store_pool(self, store_id):
        return self.store_pools[store_id]


class MockReservationProvider:
    def __init__(self):
        self.reservations = {}

    def get_reservations_with_id(self, res_id):
        reservations_obtained = []
        for res in self.reservations.values():
            reservation, _ = res[0]
            if reservation.id == res_id:
                reservations_obtained.append(reservation)
        return reservations_obtained

    def get_store_from_reservation_id(self, reservation_id):
        store_id = []
        for res in self.reservations[reservation_id]:
            store_id.append(res[1])
        return set(store_id).pop()

    def add_reservation(self, reservation, store_id):
        if reservation.id not in self.reservations.keys():
            self.reservations[reservation.id] = [(reservation, store_id)]
        else:
            self.reservations[reservation.id].append((reservation, store_id))


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.msp = MockStoreProvider()
        self.mlp = MockLaneProvider()
        self.mrp = MockReservationProvider()

        store1 = Store(
            id='store1',
            name='esselunga',
            address='milano',
        )

        store2 = Store(
            id='store2',
            name='tigros',
            address='roma',
        )

        self.msp.stores[store1.id] = store1
        self.msp.stores[store2.id] = store2

        aisle1 = Aisle(id='aisle1', categories=[], name='aisle1')
        aisle2 = Aisle(id='aisle2', categories=[], name='aisle2')

        aisle3 = Aisle(id='aisle3', categories=[], name='aisle3')
        aisle4 = Aisle(id='aisle4', categories=[], name='aisle4')

        reservation1 = Reservation(id='reservation1', user_id='user1', aisle_id=aisle1.id)
        reservation2 = Reservation(id='reservation2', user_id='user1', aisle_id=aisle2.id)
        reservation3 = Reservation(id='reservation3', user_id='user2', aisle_id=aisle3.id)
        reservation4 = Reservation(id='reservation4', user_id='user1', aisle_id=aisle4.id)

        self.mrp.add_reservation(reservation1, store1.id)
        self.mrp.add_reservation(reservation2, store1.id)
        self.mrp.add_reservation(reservation3, store2.id)
        self.mrp.add_reservation(reservation4, store2.id)

        self.mlp.aisle_pools[aisle1.id] = AislePool()
        self.mlp.aisle_pools[aisle1.id].capacity = 10
        self.mlp.aisle_pools[aisle1.id].add(reservation1.id)

        self.mlp.aisle_pools[aisle2.id] = AislePool()
        self.mlp.aisle_pools[aisle2.id].capacity = 10
        self.mlp.aisle_pools[aisle2.id].add(reservation2.id)

        self.mlp.aisle_pools[aisle3.id] = AislePool()
        self.mlp.aisle_pools[aisle3.id].capacity = 10
        self.mlp.aisle_pools[aisle3.id].add(reservation3.id)

        self.mlp.aisle_pools[aisle4.id] = AislePool()
        self.mlp.aisle_pools[aisle4.id].capacity = 10
        self.mlp.aisle_pools[aisle4.id].add(reservation4.id)

        self.mlp.store_pools[store1.id] = StorePool()
        self.mlp.store_pools[store1.id].enabled = [reservation1.id, reservation2.id]
        self.mlp.store_pools[store2.id] = StorePool()
        self.mlp.store_pools[store2.id].enabled = [reservation4.id, reservation3.id]

    def test_reservation_removed_from_correct_pools(self):
        rur = RemoveUnusedReservation(
            lane_provider=self.mlp,
            reservation_provider=self.mrp,
            store_provider=self.msp)

        rur.execute()
        self.assertEqual(len(self.mlp.store_pools['store1'].enabled), 2)
        self.assertEqual(len(self.mlp.store_pools['store2'].enabled), 2)
        self.assertEqual(len(self.mlp.aisle_pools['aisle1']), 1)
        self.assertEqual(len(self.mlp.aisle_pools['aisle2']), 1)
        self.assertEqual(len(self.mlp.aisle_pools['aisle3']), 1)
        self.assertEqual(len(self.mlp.aisle_pools['aisle4']), 1)

        rur.execute()
        self.assertEqual(len(self.mlp.store_pools['store1'].enabled), 0)
        self.assertEqual(len(self.mlp.store_pools['store2'].enabled), 0)
        self.assertEqual(len(self.mlp.aisle_pools['aisle1']), 0)
        self.assertEqual(len(self.mlp.aisle_pools['aisle2']), 0)
        self.assertEqual(len(self.mlp.aisle_pools['aisle3']), 0)
        self.assertEqual(len(self.mlp.aisle_pools['aisle4']), 0)

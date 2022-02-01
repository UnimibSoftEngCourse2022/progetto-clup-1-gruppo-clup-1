from collections import defaultdict
import unittest

from src.clup.entities.active_pool import ActivePool
from src.clup.providers.queue_provider_abc import QueueProvider
from src.clup.usecases.add_store_usecase import AddStoreUseCase


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def add_store(self, store):
        self.stores.append(store)


class MockQueueProvider(QueueProvider):
    def __init__(self):
        self.pools = defaultdict(ActivePool)

    def get_waiting_queue(self, store_id):
        raise NotImplementedError

    def get_active_pool(self, store_id):
        return self.pools[store_id]


class TestAddStoreUseCase(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockQueueProvider()
        self.store_provider = MockStoreProvider()
        self.u = AddStoreUseCase(self.store_provider, self.queue_provider)

    def test_store_is_added_to_stores(self):
        name = 'store'
        address = 'address'
        capacity = 1

        store = self.u.execute(name, address, capacity)
        stores = self.store_provider.get_stores()

        self.assertTrue(store in stores)

    def test_adding_same_store_twice_throws_value_error(self):
        name = 'store'
        address = 'address'
        capacity = 1

        self.u.execute(name, address, capacity)

        with self.assertRaises(ValueError):
            self.u.execute(name, address, 5)

    def test_name_field_of_a_store_is_empty(self):
        name = ''
        address = 'address'
        capacity = 1

        with self.assertRaises(ValueError):
            self.u.execute(name, address, capacity)

    def test_address_field_of_a_store_is_empty(self):
        name = 'store'
        address = ''
        capacity = 1

        with self.assertRaises(ValueError):
            self.u.execute(name, address, capacity)

    def test_capacity_not_negative(self):
        name = 'store'
        address = 'address'
        capacity = -1

        with self.assertRaises(ValueError):
            self.u.execute(name, address, capacity)

    def test_queue_capacity_is_the_same(self):
        name = 'store'
        address = 'address'
        capacity = 1
        store = self.u.execute(name, address, capacity)
        active_pool = self.queue_provider.get_active_pool(store.id)

        self.assertEqual(capacity, active_pool.capacity)

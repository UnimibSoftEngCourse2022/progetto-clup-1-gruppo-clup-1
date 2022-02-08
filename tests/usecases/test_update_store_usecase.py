import dataclasses
import unittest
from collections import defaultdict

from tests.usecases.mock_queue_provider import MockQueueProvider

from src.clup.entities.active_pool import ActivePool
from src.clup.entities.store import Store
from src.clup.providers.queue_provider_abc import QueueProvider
from src.clup.usecases.update_store_usecase import UpdateStoreUseCase


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def update_store(self, store):
        for store_item in self.stores:
            if store_item.id == store.id:
                args = {'name': store.name, 'address': store.address}
                dataclasses.replace(store_item, **args)


class TestUpdateStoreUseCase(unittest.TestCase):
    def setUp(self):
        self.store_provider = MockStoreProvider()
        self.queue_provider = MockQueueProvider()
        self.u = UpdateStoreUseCase(self.store_provider, self.queue_provider)
        self.store = Store(1, 'name', 'address')
        self.store_provider.stores.append(self.store)

    def test_store_is_updated_in_stores(self):
        store = Store(1, 'name1', 'address1')

        self.u.execute(store, 5)
        stores = self.store_provider.get_stores()

        self.assertTrue(self.store in stores)

    def test_update_on_unexisting_id_throws(self):
        store = Store(2, 'name1', 'address1')

        with self.assertRaises(ValueError):
            self.u.execute(store, 5)
        self.assertTrue(self.store in self.store_provider.get_stores())

    def test_name_field_of_a_store_is_empty(self):
        store = Store(1, '', 'address')

        with self.assertRaises(ValueError):
            self.u.execute(store, 5)
        self.assertTrue(self.store in self.store_provider.get_stores())

    def test_address_field_of_a_store_is_empty(self):
        store = Store(1, 'name', '')

        with self.assertRaises(ValueError):
            self.u.execute(store, 5)
        self.assertTrue(self.store in self.store_provider.get_stores())

    def test_capacity_is_not_negative(self):
        store = Store(1, 'name', 'address')

        with self.assertRaises(ValueError):
            self.u.execute(store, -1)
        self.assertTrue(self.store in self.store_provider.get_stores())

    def test_update_store_forwards_max_capacity_error(self):
        store_id = 1
        store = Store(1, 'name', 'address')
        self.queue_provider.get_active_pool(store_id).capacity = 1
        self.queue_provider.get_active_pool(store_id).add('a')

        with self.assertRaises(ValueError):
            self.u.execute(store, 0)
        self.assertTrue(self.store in self.store_provider.get_stores())

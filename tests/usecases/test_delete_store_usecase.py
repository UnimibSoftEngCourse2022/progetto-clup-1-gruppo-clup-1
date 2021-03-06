import unittest
from collections import defaultdict

from src.clup.entities.aisle_pool import AislePool
from src.clup.entities.store import Store
from src.clup.providers.abc.lane_provider import LaneProvider
from src.clup.usecases.store_manager.delete_store import DeleteStore


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def delete_store(self, store_id):
        for store in self.stores:
            if store.id == store_id:
                to_remove = store
        self.stores.remove(to_remove)


class MockQueueProvider(LaneProvider):
    def __init__(self):
        self.pools = defaultdict(AislePool)

    def get_waiting_queue(self, store_id):
        raise NotImplementedError

    def get_aisle_pool(self, store_id):
        return self.pools[store_id]


class TestDeleteStoreUseCase(unittest.TestCase):
    def test_store_is_deleted_to_stores(self):
        store_provider = MockStoreProvider()
        u = DeleteStore(store_provider)
        store = Store(1, 'name', 'address')
        store_provider.stores.append(store)

        old_stores = store_provider.get_stores()
        updated_stores = u.execute(store.id)

        self.assertEqual(old_stores, updated_stores)

    def test_delete_on_unexisting_id_throws(self):
        store_provider = MockStoreProvider()
        u = DeleteStore(store_provider)
        store = Store(1, 'name', 'address')

        with self.assertRaises(ValueError):
            u.execute(store)

    @unittest.skip('to implement in future')
    def test_delete_store_its_waiting_queue(self):
        self.fail('waiting queue not deleted')

    @unittest.skip('to implement in future')
    def test_delete_store_its_active_pool(self):
        self.fail('active pool not deleted')
